#include <unistd.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

       

///////////////////////////////////////////////////////////////////
/** \brief Definitions of constants
*
* #define constants
*/
///////////////////////////////////////////////////////////////////
#define SUCCESS 1
#define FAIL 0
#define PREAMBLE_MTK_STX0 0x04
#define PREAMBLE_MTK_STX1 0x24
#define PREAMBLE_MTK_ETX0 0x0D
#define PREAMBLE_MTK_ETX1 0x0A
#define BYTES_PER_EPO_SEG 2304
#define NUMB_SAT_PER_PACKET 3
#define BYTES_PER_SAT 72
#define BYTES_3SATS_PER_PACKT NUMB_SAT_PER_PACKET*BYTES_PER_SAT
#define NUMB_SAT_PER_EPO_SEG 32
#define MTKBIN_3EPO_PKT_LNG 227

#define PCKT253_SETPMTKPROTO_FLAG 0

#define UINT32 uint32_t
#define BYTE   uint8_t
#define DWORD  uint32_t

int epoSeq = 0;
int lastEpoSeq = 0;
int nEpoRecordSize = 0;

int epo_size;
uint8_t *epo_data = 0;

uint8_t ComputeChkSum(uint8_t *b, int n)
{
	uint8_t c = 0;
	for (int i=0; i < n; ++i, ++b) 
		c = c ^ (*b);
	return c;
}

//int fgEpo_Get_OnePkt (unsigned int seq, BYTE* pEpoRecord, BYTE* pData, int size);


#if 0
int ReadNextLine ()
{
	static uint8_t b[1024];
	static int n = 0;
	
	 
}
#endif

char * getline2 (void) {
    char * line = malloc(100), * linep = line;
    size_t lenmax = 100, len = lenmax;
    int c;

    if(line == NULL)
        return NULL;

    for(;;) {
        c = fgetc(stdin);
        if(c == EOF)
            break;

        if(--len == 0) {
            len = lenmax;
            char * linen = realloc(linep, lenmax *= 2);

            if(linen == NULL) {
                free(linep);
                return NULL;
            }
            line = linen + (line - linep);
            linep = linen;
        }

        if((*line++ = c) == '\n')
            break;
    }
    *line = '\0';
    return linep;
}



void dump_line (char *line)
{
	if (*line == '$') {
		line[strlen(line)-2] = 0; 
		fprintf (stderr, "A: %s\n", line);
	} else {
		
		// Total number bytes in the packet from Preamble to End Word.
		// Maximum packet size: 256 bytes
		// Use little endian
		// Use one byte alignment

		int len = (uint8_t)line[2] + ((uint8_t)line[3])*256; 
		fprintf (stderr, "B: %02X%02X: len: %d, ID: %02X%02X(%d) ", 
		         line[0], line[1], len,
		         line[4], line[5], (uint32_t)((uint8_t)line[4] + ((uint8_t)line[5])*256)
		        );
		        
		if (line[len-3] != ComputeChkSum((uint8_t *)(&line[2]), len - 5)) {        
            
            fprintf (stderr,  "CHK: %d should be %d\n", line[len-3] , ComputeChkSum((uint8_t *)(&line[2]), len - 5));
        } else {
			fprintf (stderr,  "CHK OK: %d\n", line[len-3]);
		}
		
		// The checksum is the 8-bit exclusive OR of all bytes 
		// in the packet between but not including 
		// the “Preamble” and the “Checksum”
		
		
		char *p = &(line[6]);
		
		for (int i = 0; i < 16; ++i, ++p)
			fprintf (stderr, "%02X ", *p);
		
		#if 0	
		p = &(line[4]);
		
		for (int i = 0; i < 16; ++i, ++p)
			fprintf (stderr, "%c ", *p);
	    #endif
	    
	    fprintf (stderr, "\n---------\n");
	}
}
/** \fn void SetBinProt(UINT32 baud)
This function builds the PMTK command string to set the UART to the
binary packet protocol
*/

void SetBinProt(UINT32 baud)
{
	char* szCmdBuf= "$PMTK253,1,115200*00\r\n";
	fwrite (szCmdBuf, strlen(szCmdBuf), 1, stdout);
	fflush (stdout);
}

/*
	Open File and Veirfy with Data Bytes
	This function to read the EPO file, and then verify the validity 
	of EPO data. 
	If the input EPO file is not in valid file length, 
	the programmer shall terminate the process.
*/

int fgEPO_Verify_File(const char* epoFileName)
{
	/**
	Open the EPO file and read the file into the allocated buffer.
	This function shall return the data bytes read from the file.
	*/
	FILE *fepo = fopen (epoFileName, "r");
	if (!fepo) {
		perror ("Unable to open EPO data\n");
		exit (255);
	}
	fseek(fepo, 0L, SEEK_END);
	int bytesRead = ftell(fepo); 
	
	fprintf (stderr, "EPO data length: %d\n", bytesRead);
	
	fseek(fepo, 0L, SEEK_SET);
	 
	epo_data = malloc ( bytesRead );
	usleep (1); 
	
	if (epo_data) {
		
		if (fread (epo_data, bytesRead, 1, fepo) == 1) {
			
			/**
			* A valid data file length must be multiples of segment length.
			* GPS: the segment length is 2304 bytes
			*/
			if ((bytesRead % BYTES_PER_EPO_SEG) != 0) {
				bytesRead = 0;
			}
		} else {
			perror ("Reading file\n");
		}
	} else {
		perror ("Reading file....\n");
		exit (255);
	}	
	return bytesRead;
}


/*
 * Get Total Number of Packets
 * 
 * This function to get total number of MTK_BIN_EPO packets that
 * will be sent in EPO_Get_Num_Pkt function.
 *
 */
 
int EPO_Get_Num_Pkt(int recordLen)
{
	int retVal = 0;
	if (recordLen != 0) {
		int numbOfSet = recordLen/BYTES_PER_EPO_SEG;
		retVal = (numbOfSet*NUMB_SAT_PER_EPO_SEG)/NUMB_SAT_PER_PACKET;
	}
	return retVal;
}


/*
Build Data Packets
This function, fgEPO_Get_One_Pkt(…), takes out three SAT data from the SGEE-EPO data file and
encapsulated them in a MTK_BIN_EPO packet with appropriate EPO SEQ number.
* 
* 
* 
*/

int fgEpo_Get_OnePkt(unsigned int seq, const BYTE* pEpoRecord, int epoSize, BYTE* pData, int size)
{
	int retVal = FAIL;
	/*
	Sanity check the input argument
	 */
	// [CODE]
	if ((seq+1)*BYTES_3SATS_PER_PACKT <= epoSize) {
		int indx = 0;
		pData[indx++] = PREAMBLE_MTK_STX0;
		pData[indx++] = PREAMBLE_MTK_STX1;
		pData[indx++] = 0xE3;
		pData[indx++] = 0x0;
		pData[indx++] = 0xD3;
		pData[indx++] = 0x02;
		pData[indx++] = seq & 0xFF;
		pData[indx++] = (seq >> 8) & 0xFF;
		memcpy ((BYTE*)&(pData[indx]), 
		        (BYTE*)&(pEpoRecord[seq*BYTES_3SATS_PER_PACKT]),
		        BYTES_3SATS_PER_PACKT
		        );
		        
		indx += BYTES_3SATS_PER_PACKT;
		//* len byte + Cmd byte + Seq byte = 6
		BYTE chksum = ComputeChkSum(pData+2, 6 + BYTES_3SATS_PER_PACKT); 
		pData[indx++] = chksum;
		pData[indx++] = PREAMBLE_MTK_ETX0;
		pData[indx++] = PREAMBLE_MTK_ETX1;
		retVal = SUCCESS;
	}
	return retVal;
}

/*
 * 
 * Get Packets and Send
 * This function is to start SGEE-EPO data transfer protocol
 * to send SGEE-EPO data.
 * 
 */

void EMOD_DLEng (int numPkt, DWORD epoSize, const BYTE *pEPOBuff)
{
	uint8_t dataBuf [1024];
	
	fprintf (stderr, "Loop: \r\n");
	epoSeq = 0;
	for (int i = 0; i < numPkt; i++) {
		if (fgEpo_Get_OnePkt(epoSeq, pEPOBuff, epoSize, dataBuf, sizeof(dataBuf)) == SUCCESS) {
			//* Send the current packet
			fwrite (dataBuf, MTKBIN_3EPO_PKT_LNG, 1, stdout);
			fflush (stdout);
			//* Update the last Epo SEQ number
			lastEpoSeq = epoSeq;
			epoSeq++;
			
			usleep (10000);
			fprintf (stderr, "%d\r", i);
			char * ll = getline2();
			dump_line(ll);
		}
	}
	fprintf (stderr, "\r\n");
}

#if 0
int fgEpo_Get_OnePkt_2(unsigned int seq, BYTE* pEpoRecord, BYTE* pData, int size)
{
	int retVal = FAIL;
	/**
	 * Sanity check the input argument
	 */
	// [CODE]
	if ((seq+1)*BYTES_3SATS_PER_PACKT <= epo_size) {
		
	} else {
		int trailBytes = nEpoRecordSize - seq * BYTES_3SATS_PER_PACKT;
		if ((trailBytes % 72) == 0) {
			int indx = 0;
			BYTE fillBytes[BYTES_3SATS_PER_PACKT]; 

			// To prefill the bytes with numerial 0
			memset (fillBytes, 0x30, sizeof(fillBytes));
			
			memcpy((BYTE*)&(fillBytes[0]),(BYTE*)&(pEpoRecord[seq*BYTES_3SATS_PER_PACKT]), trailBytes);
			
			pData[indx++] = PREAMBLE_MTK_STX0;
			pData[indx++] = PREAMBLE_MTK_STX1;
			pData[indx++] = 0xE3;
			pData[indx++] = 0x0;
			pData[indx++] = 0xD3;
			pData[indx++] = 0x02;
			pData[indx++] = seq & 0xFF;
			pData[indx++] = (seq >> 8) & 0xFF;
			
			memcpy((BYTE*)&(pData[indx]), (BYTE*)&fillBytes[0],	BYTES_3SATS_PER_PACKT);
			indx += BYTES_3SATS_PER_PACKT;
			BYTE chksum = ComputeChkSum(pData+2, 6 + BYTES_3SATS_PER_PACKT); //* len byte + Cmd byte + Seq byte = 6
			pData[indx++] = chksum;
			pData[indx++] = PREAMBLE_MTK_ETX0;
			pData[indx++] = PREAMBLE_MTK_ETX1;
			
			retVal = SUCCESS;
		}
	}
	return retVal;
}
#endif

/*
Send current MTK_BIN_EPO packet. The packet size of MTK_BIN_EPO is
MTKBIN_3EPO_PKT_LNG.
The call to OutputBytes() must be made by the programmer.
*/
void SendData(BYTE* pData, int dataLen)
{
	fwrite (pData, 1, dataLen, stdout);
	fflush (stdout);
}

/*
 * Build Final Data Packet
 * Generate final MTK_BIN_EPO packet to indicate the GPS receiver
 * that the process is finish.
*/

int vEPO_GET_Final_Pkt(BYTE* pData, int size)
{
	//int retVal = FAIL;
	//BYTE val = 0;
	int indx = 0;
	/**
	 * Sanity check the input argument
	 */
	// [CODE]
	
	pData[indx++] = PREAMBLE_MTK_STX0;
	pData[indx++] = PREAMBLE_MTK_STX1;
	pData[indx++] = 0xE3;
	pData[indx++] = 0x0;
	pData[indx++] = 0xD3;
	pData[indx++] = 0x02;
	pData[indx++] = 0xFF;
	pData[indx++] = 0xFF;
	memset((BYTE*)&(pData[indx]), 0, BYTES_3SATS_PER_PACKT);
	indx += BYTES_3SATS_PER_PACKT;
	
	pData[indx++] = ComputeChkSum(pData+2, 6 + BYTES_3SATS_PER_PACKT);
		
	pData[indx++] = PREAMBLE_MTK_ETX0;
	pData[indx++] = PREAMBLE_MTK_ETX1;
	
	return indx;
}

/*
Build Packet and Change Port to ASCII mode
Switch UART protocol setting to ASCII mode and baudrate 115200.

0x04 0x24 0x0E 0x00 0xFD 0x00 0x00 0x00 0xC2 0x01 0x00 0x30 0x0D 0x0A


*/

int SetTextProt(UINT32 baud)
{
	int indx = 0;
	BYTE cmd[200] = { 0 };
	cmd[indx++] = 0x04; //* Preamble
	cmd[indx++] = 0x24;
	cmd[indx++] = 0x0E; //* Len 2 bytes for MTK_BIN_EPO packet
	cmd[indx++] = 0x00;
	cmd[indx++] = 0xFD; //* Command ID for MTK_BIN_EPO packet
	cmd[indx++] = 0x00;
	cmd[indx++] = 0x00; //PCKT253_SETPMTKPROTO_FLAG; //* PMTK protocol
	cmd[indx++] = 0x00; //(baud >> 24) & 0x000000FF;
	cmd[indx++] = 0xC2; //(baud >> 8) & 0x000000FF;
	cmd[indx++] = 0x01; //(baud >> 16) & 0x000000FF;
	cmd[indx++] = 0x00; //baud & 0x000000FF;
	cmd[indx++] = 0x30; //ComputeChkSum(&cmd[2], indx-2);
	cmd[indx++] = 0x0D;
	cmd[indx++] = 0x0A;
	int rc = fwrite (cmd, 1, indx, stdout);
	fflush (stdout);
	fprintf (stderr, "%02X", ComputeChkSum(cmd+2, 9) );
	return rc;
}



int SetTextProt2(UINT32 baud)
{
	int indx = 0;
	BYTE cmd[200] = { 0 };
	cmd[indx++] = 0x04; //* Preamble
	cmd[indx++] = 0x24;
	cmd[indx++] = 0x0E; //* Len 2 bytes for MTK_BIN_EPO packet
	cmd[indx++] = 0x00;
	cmd[indx++] = 0xFD; //* Command ID for MTK_BIN_EPO packet
	cmd[indx++] = 0x00;
	cmd[indx++] = 0x00; //PCKT253_SETPMTKPROTO_FLAG; //* PMTK protocol
	cmd[indx++] = 0x00; //(baud >> 24) & 0x000000FF;
	cmd[indx++] = 0x00; //(baud >> 8) & 0x000000FF;
	cmd[indx++] = 0x00; //(baud >> 16) & 0x000000FF;
	cmd[indx++] = 0x00; //baud & 0x000000FF;
	cmd[indx++] = 0xF3; //ComputeChkSum(&cmd[2], indx-2);
	cmd[indx++] = 0x0D;
	cmd[indx++] = 0x0A;
	int rc = fwrite (cmd, 1, indx, stdout);
	fflush (stdout);
	fprintf (stderr, "%02X", ComputeChkSum(cmd+2, 9) );
	return rc;
}


/*
Start EPO Download Function
Now the data in the data port will be viewed as Binary Packet format. 
Please create a thread to transmit
receive binary packets for the data port.
*/ 
void startEPODownload ()
{

/** Allocate buffer for the EPO data

 * Call EPO download engine, with passing parameters
	- pEPOBuffer: EPO data buffer
	- fSize: EPO data size
	- numPkts: number og packets to send
	- nBaudRate: the current baud rate
*/
	//EMOD_DLEng(nBaudRate, numPkts, fSize, pEPOBuff);
}


int main (int argc, const char *argv[])
{
	freopen(NULL, "wb", stdout);
    freopen(NULL, "rb", stdin);
	if (argc > 1) {
			
		int rc = fgEPO_Verify_File (argv[1]);
	
		fprintf (stderr, "Bytes: %d\n", rc);
		
		epo_size = rc;
		
		fprintf (stderr, "Records: %f\n", (float)rc / BYTES_PER_EPO_SEG);
		
		int npac = EPO_Get_Num_Pkt(rc);
		
		fprintf (stderr, "packets: %d\n", npac);
		
		SetBinProt(115200);
	  
		usleep (1000000); // 1 sec
		
		// EMOD_DLEng (npac, epo_size, epo_data);
		
		
		uint8_t pData [1000];
		int n = vEPO_GET_Final_Pkt(pData, sizeof(pData));
		fwrite (pData, n, 1, stdout);
		fflush (stdout);
		
	} else {

	}
	usleep (10000); // 10 ms
	fprintf (stderr, "recover text mode....");
	int rc = SetTextProt(115200);
	fprintf (stderr, " %d bytes written\n", rc);
	fprintf (stderr, "Exiting.....\n\n");
	return 0;
}
