#include <unistd.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>


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
void dump_line (char *line);


typedef struct {
	int  s;
	char line[10240];
	int  n;
} TH_DATA;

#if 1
static void * ReadNextLine (void *arg)
{
	TH_DATA *p = (TH_DATA *) arg;
	
	fprintf (stderr, "Thread started.... %s %d\n", 
	         p->line, p->s);
	         
	for (;p->s;) {

        int rc = read (p->s, &(p->line [p->n]), 1);
        
        if (rc < 0) {
           if (errno == EAGAIN) {
               usleep (100000); // 100 ms
               continue;
           } else {
               fprintf (stderr, "%d: %d.%s\n", rc, errno, strerror(errno));
               break;
           }
        }
        //fprintf (stderr, "%02x ", p->line [p->n]);
        p->line [p->n + 1] = 0;

        if (p->line [p->n] == 10) {
			//fprintf (stderr, " LEN: %d\n", p->n+1);
			dump_line (p->line);
            p->n = 0;
            memset (p->line, 0, sizeof(p->line));
		} else {
		    p->n = p->n + 1;
		}
	}
	perror ("Serial ");
	fprintf (stderr, "Thread exiting....\n");

	return 0;
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
		fprintf (stderr, "A: [%s]\n", line);
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

/** \fn void SetBinProt(UINT32 baud)
This function builds the PMTK command string to set the UART to the
binary packet protocol
*/

void SetBinProt(UINT32 baud, int s)
{
	//char* szCmdBuf= "$PMTK253,1,115200*00\r\n";
	char* szCmdBuf= "$PMTK253,1,0*37\r\n";
	write (s, szCmdBuf, strlen(szCmdBuf));
	
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

void EMOD_DLEng (int numPkt, DWORD epoSize, const BYTE *pEPOBuff, int ser)
{
	uint8_t dataBuf [1024];
	
	fprintf (stderr, "Loop: \r\n");
	epoSeq = 0;
	for (int i = 0; i < numPkt; i++) {
		if (fgEpo_Get_OnePkt(epoSeq, pEPOBuff, epoSize, dataBuf, sizeof(dataBuf)) == SUCCESS) {
			//* Send the current packet
			int rc = write (ser, dataBuf, MTKBIN_3EPO_PKT_LNG);
			
			if (rc != MTKBIN_3EPO_PKT_LNG) {
				fprintf (stderr, "%d: %d.%s\n", rc, errno, strerror(errno));
				break;
			}
			//* Update the last Epo SEQ number
			lastEpoSeq = epoSeq;
			epoSeq++;
			
			usleep (100000/4);
			fprintf (stderr, "***************** %d\r", i);
		}
	}
	fprintf (stderr, "\r\n");
}
//
// 0x04 0x24 0x0E 0x00 0xFD 0x00 0x00 0x00 0xC2 0x01 0x00 0x30 0x0D 0x0A
//
int SetTextProt (UINT32 baud, int s)
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
	int rc = write (s, cmd, indx);
	if (rc != indx) {
		fprintf (stderr, "%d: %d.%s\n", rc, errno, strerror(errno));
	} else {	
		fprintf (stderr, "%02X", ComputeChkSum(cmd+2, 9) );
	}
	return rc;
}



int SetTextProt2 (UINT32 baud, int s)
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
	int rc = write (s, cmd, indx);
	
	fprintf (stderr, "%02X", ComputeChkSum(cmd+2, 9) );
	return rc;
}

const char *serial = "/dev/ttyS2";

int main (int argc, const char *argv[])
{
    pthread_t thread_id;
 
    fprintf (stderr, "set serial in RAW mode, N81, no hw handshake, 115200 bps\n");   
    char cmd [1024];
    snprintf (cmd, sizeof(cmd), "/bin/stty  -F %s ispeed 115200 ospeed 115200 -crtscts cs8 min 0 time 100 raw", serial);
    system (cmd);
    
    //FILE *ser = fopen (serial, "rw+");
    int ser;                                   /* File descriptor for the port */

    ser = open(serial, O_RDWR | O_NOCTTY | O_NDELAY);

    if (ser == -1)  {                                              /* Could not open the port */
       fprintf(stderr, "open_port: Unable to open %s - %s\n",
               serial, strerror(errno));
    }

    
	TH_DATA *pd = malloc (sizeof(TH_DATA));
	memset(pd, 0, sizeof(TH_DATA));
    pd->s = ser;
    strcpy (pd->line, serial);
    
    pthread_create(&thread_id, 0, &ReadNextLine, pd);
               
    usleep (2000000); // 2 sec
	
    SetBinProt(115200, ser);
	fprintf (stderr, "*************** BINARY ***************\n");
	usleep (5000000); // 5 sec
		
		
	if (argc > 1) {
			
		int rc = fgEPO_Verify_File (argv[1]);
	
		fprintf (stderr, "Bytes: %d\n", rc);
		
		epo_size = rc;
		
		fprintf (stderr, "Records: %f\n", (float)rc / BYTES_PER_EPO_SEG);
		
		int npac = EPO_Get_Num_Pkt(rc);
		
		fprintf (stderr, "packets: %d\n", npac);
		
		EMOD_DLEng (npac, epo_size, epo_data, ser);
			
		fprintf (stderr, "*************** END OF BINARY STREAM ***************\n");
		uint8_t pData [1000];
		int n = vEPO_GET_Final_Pkt(pData, sizeof(pData));
		write (ser, pData, n);
		fprintf (stderr, "*************** END OF STREAM SENT ***************\n");
	}                       
    fprintf (stderr, "recover text mode....");
    
	int rc = SetTextProt2(115200, ser);
	
	fprintf (stderr, " %d bytes written\n", rc);
	
	usleep(2000000);
	
    //fprintf (stderr, "recover text mode....");
    
	//rc = SetTextProt(115200, ser);
	
	//fprintf (stderr, " %d bytes written\n", rc);
	
	usleep(2000000);
	
    
	fprintf (stderr, "Exiting.....\n\n");
	
	close (pd->s);
	pd->s = 0;
	
	pthread_join (thread_id, 0);
	return 0;
}
