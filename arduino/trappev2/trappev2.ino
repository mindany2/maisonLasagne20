#define MAX 100
#define TEMPS_ATTENTE 50 


int compt = MAX;      // si le compteur est à 0 on commence la séquence de monter ou descendre

int deja_en_interrupt = false;

void pciSetup(byte pin)
{
    *digitalPinToPCMSK(pin) |= bit (digitalPinToPCMSKbit(pin));  // enable pin
    PCIFR  |= bit (digitalPinToPCICRbit(pin)); // clear any outstanding interrupt
    PCICR  |= bit (digitalPinToPCICRbit(pin)); // enable interrupt for the group
}



//ISR (PCINT1_vect) // handle pin change interrupt for A0 to A5 here
ISR (PCINT0_vect) // handle pin change interrupt for D8 to D13 
{
  if (not(deja_en_interrupt)){
    deja_en_interrupt = true;
    if(digitalRead(A1) == LOW){
      Serial.print("rdc : descente \n");
    }
    else if(digitalRead(A2) == LOW){
      Serial.print("rdc : montee \n");
    }
    else if(digitalRead(A3) == LOW){
      Serial.print("etage : monte \n");
    }
    else if(digitalRead(A4) == LOW){
      Serial.print("etage : descente \n");
    }
    else if(digitalRead(A5) == LOW){
      Serial.print("capteur \n");
    }
    delay(20000);
    deja_en_interrupt = false;
  }
}


void setup() {
  int i;
  Serial.begin(9600);
  Serial.print("coucou\n");
 
  // set pullups, if necessary
  for (i=A1; i<=A5; i++)
      digitalWrite(i,HIGH);
 
  // enable interrupt for pin...
  pciSetup(A1);
  /*
  pciSetup(A2);
  pciSetup(A3);
  pciSetup(A4);
  pciSetup(A5);
*/
}

void loop()
{ 
  /*
  if (compt == 0){ // on commence par lancer le gyro
    digitalWrite(gyrophare_haut,LOW);
  }
  else if(compt == TEMPS_ATTENTE){ // au bout de 5s on lance l'action
    if (on_monte){
      digitalWrite(distrib_monte,LOW);
      delay(50); 
      digitalWrite(distrib_monte,HIGH);
    }
    else{
      digitalWrite(distrib_descente,LOW);
      delay(50);
      digitalWrite(distrib_descente,HIGH);
    }
  }
  else if(compt == MAX){  // a la fin on eteint le gyro
     digitalWrite(gyrophare_haut,HIGH);
  }

  if (compt < MAX){
    Serial.println(compt);
    compt ++; // on incrémente
  }
  delay(100); // fréquence des actions, toute les secondes
  */
}
