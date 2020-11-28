#define capteur_fermeture 13
#define distrib_descente 12
#define distrib_montee 11
#define gyro 10
#define aimant 9
#define securite 8


#define MAX 250

void pciSetup(byte pin)
{
    *digitalPinToPCMSK(pin) |= bit (digitalPinToPCMSKbit(pin));  // enable pin
    PCIFR  |= bit (digitalPinToPCICRbit(pin)); // clear any outstanding interrupt
    PCICR  |= bit (digitalPinToPCICRbit(pin)); // enable interrupt for the group
}
 

int count = MAX;

int deja_en_interrupt = false;
bool on_monte = true; // 1 = ouverture , 0 = fermeture

int etat_trappe() { // 1 = ouvert / 0 = ferme
   return digitalRead(capteur_fermeture);
}

void ouverture(){
  if (not(etat_trappe()) and count == MAX){ //si je suis ferme
    on_monte = true;
    count = 0;
  }
  else if (count < MAX and not(on_monte)){ // on reouvre rapidement
    if (count > 50){ // on agit direct
      on_monte = true;
      count = 50;
    }
    else{ // on fait rien
      on_monte = true;
      count = MAX;
    }
  }
}

void fermeture(){
  if (etat_trappe() and count == MAX){ //si je suis ferme
    on_monte = false;
    count = 0;
  }
  else if (count < MAX and on_monte){ // on reouvre rapidement
    if (count > 50){ // on agit direct
      on_monte = false;
      count = 50;
    }
    else{ // on fait rien
      count = MAX;
      on_monte = false;
    }
  }
}

ISR (PCINT0_vect) // handle pin change interrupt for D8 to D13 here
 {    
 } 

ISR (PCINT1_vect) // handle pin change interrupt for A0 to A5 here
{ 
  if (digitalRead(securite) == LOW){
    if (digitalRead(A1) == LOW){
      Serial.print("rdc : montee\n");
      ouverture();
    }
    else if (digitalRead(A2) == LOW){
      Serial.print("rdc : descente\n");
      fermeture();
    }
    else if (digitalRead(A3) == LOW){
      Serial.print("etage : montee\n");
      ouverture();
    }
    else if (digitalRead(A4) == LOW){
      Serial.print("etage : descente\n");
      fermeture();
    }
    delay(1000);
  }
}


void setup() {
  int i;
  Serial.begin(9600);
  Serial.print("coucou\n");
 
  for (i=A0; i<=A4; i++)
      digitalWrite(i,HIGH);
 
  // enable interrupt for pin...
  pciSetup(A1);
  pciSetup(A2);
  pciSetup(A3);
  pciSetup(A4);

  pinMode(distrib_montee, OUTPUT);
  pinMode(distrib_descente, OUTPUT);
  pinMode(gyro, OUTPUT);
  pinMode(aimant, OUTPUT);

  digitalWrite(distrib_montee,HIGH);
  digitalWrite(distrib_descente,HIGH);
  digitalWrite(gyro,HIGH);

  if (etat_trappe()){ // ouverte
    digitalWrite(aimant,HIGH);
  }
  else {
    digitalWrite(aimant,LOW);
  }
  


  Serial.println(etat_trappe());
  
}

void loop()
{ 
  if (count == 0){
      digitalWrite(gyro,LOW);
      if (not(on_monte)){
         digitalWrite(aimant,LOW); // on decolle l'aimant
      }
  }
  else if (count == 50){
    if (on_monte){ // on monte
      digitalWrite(distrib_montee,LOW);
      delay(100);
      digitalWrite(distrib_montee,HIGH);
    }
    else{
      digitalWrite(distrib_descente,LOW);
      delay(100);
      digitalWrite(distrib_descente,HIGH);
    }
  }
  else if (count == MAX){
     digitalWrite(gyro,HIGH);
     if (on_monte){
         digitalWrite(aimant,HIGH); // on colle l'aimant
      }
  }
  else if (count == 150 and not(on_monte)){ // plus rapide a descendre qu'a monter
     digitalWrite(gyro,HIGH);
     count = MAX;
  }

  if (count < MAX){
    count ++;
  }
  delay(100);
}
