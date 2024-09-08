#include <Arduino.h>
#include <TimerOne.h>
  
   

#define LED1 13
#define interruptPin 2

byte gpioInputList[][8] = {{54,55,56,57,58,59,60,61},{62,63,64,65,66,67,68,69}};
byte gpioOutputList[][8] = {{22,23,24,25,26,27,28,29},{30,31,32,33,34,35,36,37}};


volatile int byteCounter = 0;
volatile boolean DataState = false;
volatile byte Data[10];


volatile boolean rcvDataState = false;
volatile byte rcvData = 100;

void run(unsigned char Data_array[],int nbytes) {
  Serial.println("in run()");
  for (int i = 0 ; i< nbytes; i = i+3){
    for (int z = i; z < i+3; z++)
    {
      int value = Data_array[z];
      Serial.println(value);
    }
    Serial.println(bitRead(Data_array[i],4));
    if (bitRead(Data_array[i],4)  == 1){
      Serial.println("Intimer func:");
      for (int  j = 0; j < 2; j++){
        for (int k = 0; k < 8; k++){
          digitalWrite(gpioOutputList[j][k],bitRead(Data_array[i+j+1],k));
        }
        
      }
      int waittime = Data_array[i] & 0b1111;
      Serial.println(waittime);
      delay(waittime*1000);
    }
    
  }
  
}


boolean read () {
  int nBytes;
  
  if (Serial.available()) {
    Serial.write("#");
    digitalWrite(LED1,!digitalRead(LED1));
    if (Serial.read() == 255){
      nBytes = Serial.read();
      
      byteCounter = nBytes;
      unsigned char Data_[nBytes];
      for (int i = 0; i < nBytes; i++){
        Data_[i] = Serial.read();
      }
      DataState = true;

      run(Data_,nBytes);
    //reset
    for (int i = 0; i < 2; i++){
      for (int j = 0; j < 8; j++){
        digitalWrite(gpioOutputList[i][j],0);     
    }
    
  }
      
      
    }
  }else {
    
  }

  return true;
}

boolean write () {
    if (rcvDataState){
      Serial.write(rcvData);
      rcvDataState = false;
    }
    return true;
}


void writePins () {
  digitalWrite(LED1,!digitalRead(LED1));
}

void readPins () {
  Timer1.stop(); //test
  
  rcvDataState = true;
  
}




void setup() {
  for (int i = 0; i < 2; i++){
    for (int j = 0; j < 8; j++){
      pinMode(gpioInputList[i][j],INPUT);
      pinMode(gpioOutputList[i][j],OUTPUT);
      
      digitalWrite(gpioOutputList[i][j],0);     
    }
    
  }
  
  

  Serial.begin(115200);
  pinMode(13,OUTPUT);

  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), readPins, CHANGE);

  // Timer1.initialize(2000000);  //  runs every 2 seconds
  // Timer1.attachInterrupt(writePins); 
  
}


void loop() {
  
  read();
  delay(1000);
  
 
}