#include <Stepper.h> 

/* Pin Initializations  */

#define DIR_X 16 
#define STEP_X 17
#define ENABLE_X 23

#define DIR_Y 34
#define STEP_Y 35
#define ENABLE_Y 41

#define DIR_Z 24
#define STEP_Z 25
#define ENABLE_Z 31 

#define EM_PIN 9 

/* Code Parameters */

#define STEPS_PER_SQUARE 40000

#define STEPS_PER_REV 100
#define LED 13

#define MAX_STEP_SPEED 1000 // Maximum speed (steps / second)

#define DELAY 500
#define TEST_STEPS 2500

/* Code Global Variables */

int currentSquareX = 1;
int currentSquareY = 1;
int startSquareX = 1;
int startSquareY = 1; 
int endSquareX = 1;
int endSquareY = 1; 

String inputString = ""; 

/* Initialize stepper drivers */

Stepper stepperX(STEPS_PER_REV, DIR_X, STEP_X);
Stepper stepperY(STEPS_PER_REV, DIR_Y, STEP_Y);
Stepper stepperZ(STEPS_PER_REV, DIR_Z, STEP_Z);

void setup() {
  Serial.begin(115200);
  
  pinMode(ENABLE_X, OUTPUT);
  pinMode(ENABLE_Y, OUTPUT);
  pinMode(ENABLE_Z, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(EM_PIN, OUTPUT);

  stepperX.setSpeed(MAX_STEP_SPEED);
  stepperY.setSpeed(MAX_STEP_SPEED);
  stepperZ.setSpeed(MAX_STEP_SPEED);

  digitalWrite(ENABLE_X, LOW); // Enable stepper driver
  digitalWrite(ENABLE_Y, LOW); 
  digitalWrite(ENABLE_Z, LOW);  
  digitalWrite(EM_PIN, LOW); // Start with EM off

  delay(100);
}

void loop() {  
  /*processStringCommand(); // Waits until a serial input, then stores start and end x / y positions in global variables

  driveCurrentToFinal(); // Moves piece from starting to ending position, while energizing electromagnet as appropriate*/

  /*electromagnetControl(false);
  stepSquareX(1);
  stepSquareY(1);
  delay(1000);
  electromagnetControl(true);
  stepSquareX(-1);
  stepSquareY(-1);
  delay(1000);*/
    
  double motionAmount = 0.005;
  for (int i = 0; i < 400; i++){
    stepSquareX(-1.*motionAmount);
    stepSquareY(-1.*motionAmount);
  }
  delay(2000);
  /*for (int i = 0; i < 500; i++){
    stepSquareX(0*motionAmount);
    stepSquareY(0*motionAmount);
  }
  delay(2000);*/

  stepSquareZ(1);
  delay(2000);
  //stepSquareZ(-4);
  //delay(2000);*/

}

void stepSquareX(double squareQuantity){
  // Move x-axis motor by a given amount of squares
  int numSteps = (int)(squareQuantity * (double)STEPS_PER_SQUARE);
  stepperX.step(numSteps);
}

void stepSquareY(double squareQuantity){
  // Move y-axis motor by a given amount of squares
  int numSteps = (int)(squareQuantity * (double)STEPS_PER_SQUARE);
  stepperY.step(numSteps);
}

void stepSquareZ(double squareQuantity){
  // Move z-axis motor by a given amount of squares
  int numSteps = (int)(squareQuantity * (double)STEPS_PER_SQUARE);
  stepperZ.step(numSteps);
}

void enterPiece(){
  stepSquareX(0.5);
  stepSquareY(0.5);
}

void exitPiece(){
  stepSquareX(-0.5);
  stepSquareY(-0.5);
}

void driveCurrentToFinal(){
  // Electromagnet starts at currentSquare, moves to startSquare, energizes, moves to endSquare, de-energizes
  
  if (currentSquareX != endSquareX || currentSquareY != endSquareY){ // Check if piece motion if needed

    Serial.println("Carraige leaving current position.");
    exitPiece(); // Piece exits current square
    stepSquareX(startSquareX - currentSquareX);
    stepSquareY(startSquareY - currentSquareY);
    electromagnetControl(true); // Chess piece picked up
    Serial.println("Carraige arrived at piece starting position. EM on");
  
    stepSquareX(endSquareX - startSquareX);
    stepSquareY(endSquareY - startSquareY);
    electromagnetControl(false); // Check piece dropped off
    enterPiece(); // Piece enters final square
    Serial.println("Carraige arrived at piece ending position. EM off");
  
    currentSquareX = endSquareX;
    currentSquareY = endSquareY; 

  }
}

void processStringCommand(){
  // Read in string input and set startSquareX, startSquareY, endSquareX, endSquareY

  while(Serial.available() <=0){
    // Wait until a new command is recieved
  }
  inputString = Serial.read(); // Input string format: "#,#,#,#" --> startSquareX,startSquareY, endSquareX, endSquareY
  // Figure out how to cache two strings. readUntil?

  // ex. "B6,A8"

  switch(inputString[0]){
    case('A'):
      startSquareX = 1;
      break;
    case('B'):
      startSquareX = 2;
      break;
    case('C'):
      startSquareX = 3;
      break;
    case('D'):
      startSquareX = 4;
      break;
    case('E'):
      startSquareX = 5;
      break;
    case('F'):
      startSquareX = 6;
      break;
    case('G'):
      startSquareX = 7;
      break;
    case('H'):
      startSquareX = 8;
      break;
  }
  startSquareY = (int)inputString[1];
  switch(inputString[3]){
    case('A'):
      endSquareX = 1;
      break;
    case('B'):
      endSquareX = 2;
      break;
    case('C'):
      endSquareX = 3;
      break;
    case('D'):
      endSquareX = 4;
      break;
    case('E'):
      endSquareX = 5;
      break;
    case('F'):
      endSquareX = 6;
      break;
    case('G'):
      endSquareX = 7;
      break; 
    case('H'):
      endSquareX = 8;
      break;
  }
  endSquareY = (int)inputString[4]; 
}

void electromagnetControl(bool onOff){
  // If onOff is true, EM is turned on; else off
  digitalWrite(EM_PIN, onOff);
}

// TO DO: see if another stepper driver is needed
// TO DO: limit switches for setting offset of stepper motor
