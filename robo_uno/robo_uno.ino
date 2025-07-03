#include <Servo.h>

Servo garraServo;
Servo punhogiroServo;
Servo punhoServo;
Servo ombroServo;
Servo bracoServo;
Servo cotoveloServo;
Servo baseServo;

int pos;
const int botao = 13;
const int botao_2 = 7;
const int led = 12;
const int led_2 = 8;

unsigned long tempoAnterior = 0;
bool estadoLed = false;

unsigned long tempoAnterior_2 = 0;
bool estadoLed_2 = false;

void setup() {
cotoveloServo.attach(11);
  cotoveloServo.write(90);

  punhoServo.attach(10);
  punhoServo.write(120);
  punhogiroServo.attach(9);
  punhogiroServo.write(0);

  ombroServo.attach(6);
  ombroServo.write(0);

  garraServo.attach(5);
  garraServo.write(0);

  baseServo.attach(3);
  baseServo.write(0);

  pinMode(botao, INPUT_PULLUP);    // botão com resistor pull-up
  pinMode(botao_2, INPUT_PULLUP);  // botão com resistor pull-up
  pinMode(led, OUTPUT);
  pinMode(led_2, OUTPUT);

}

void loop() {
if (digitalRead(botao) == LOW) {  // botão pressionado
    if (millis() - tempoAnterior >= 500) {
      tempoAnterior = millis();
      estadoLed = !estadoLed;
      digitalWrite(led, estadoLed);
    }
  } else {
    digitalWrite(led, HIGH);  // botão solto, LED apagado
    estadoLed = false;
  }
  //******************************************************************************************
  if (digitalRead(botao_2) == LOW) {  // botão 2 pressionado
    if (millis() - tempoAnterior_2 >= 500) {
      tempoAnterior_2 = millis();
      estadoLed_2 = !estadoLed_2;
      digitalWrite(led_2, estadoLed_2);
    }
  } else {
    digitalWrite(led_2, HIGH);  // botão 2 solto, LED apagado
    estadoLed_2 = false;
  }

  //******************************************************************************************
  if (digitalRead(13) == HIGH)

  {

     digitalWrite(12, HIGH);
    digitalWrite(8, LOW);
    //step 1
   // Abre Garra
    for (pos = 10; pos < 90; pos++) {
      garraServo.write(pos);
      delay(50);
    }
    delay(1000);

    //Cotovelo Recua
    for (pos = 90; pos < 130; pos++) {
      cotoveloServo.write(pos);
      delay(120);
    }
    delay(1000);

    // Ombro Avança
    for (pos = 0; pos < 70; pos++) {
      ombroServo.write(pos);
      delay(50);
    }
    delay(1000);

// Fecha Garra
    for (pos = 90; pos >= 5; pos--) {
      garraServo.write(pos);
      delay(120);
    }
    delay(1000);

    //step 2
    //Cotovelo avanca
      for (pos = 130; pos >=70; pos--) {
      cotoveloServo.write(pos);
      delay(120);
    }
    delay(1000);

    // volta ombro
      for (pos = 70; pos >= 0; pos--) {
      ombroServo.write(pos);
      delay(80);
    }
    delay(1000);

    // gira base
     for (pos = 0; pos < 90; pos++) {
      baseServo.write(pos);
      delay(50);
    }
    delay(1000);

    //step 3 
        //Cotovelo Recua
    for (pos = 70; pos < 120; pos++) {
      cotoveloServo.write(pos);
      delay(120);
    }
    delay(1000);

    // Ombro Avança
        for (pos = 0; pos < 90; pos++) {
      ombroServo.write(pos);
      delay(50);
    }
    delay(1000);


      // Punho Avança
    for (pos = 0; pos < 90; pos++) {
      punhoServo.write(pos);
      delay(50);
    }
    delay(1000);

          // Punho giro Avança
    for (pos = 0; pos < 90; pos++) {
      punhogiroServo.write(pos);
      delay(50);
    }
    delay(1000);

        // Ombro Avança
        for (pos = 90; pos < 130; pos++) {
      ombroServo.write(pos);
      delay(50);
    }
    delay(1000);

        // Abre Garra
    for (pos = 10; pos < 90; pos++) {
      garraServo.write(pos);
      delay(50);
    }
    delay(1000);

    //step 4

      // Fecha Garra
    for (pos = 90; pos >= 5; pos--) {
      garraServo.write(pos);
      delay(120);
    }
    delay(1000);

        // volta ombro
      for (pos = 130; pos >= 0; pos--) {
      ombroServo.write(pos);
      delay(80);
    }
    delay(1000);

        //Cotovelo avanca
      for (pos = 120; pos >=90; pos--) {
      cotoveloServo.write(pos);
      delay(120);
    }
    delay(1000);

         // Punho giro volta
    for (pos = 90; pos >= 0; pos--) {
      punhogiroServo.write(pos);
      delay(50);
    }
    delay(1000);

         // Punho volta
    for (pos = 90; pos >= 0; pos--) {
      punhoServo.write(pos);
      delay(50);
    }
    delay(1000);
  }
}
