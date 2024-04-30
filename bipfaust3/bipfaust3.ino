//faust code

#include <Audio.h>
#include <stdio.h>
#include <stdlib.h> 
#include "faust3.h"

faust3 faust3;
AudioOutputI2S out;
AudioControlSGTL5000 audioShield;
AudioConnection patchCord0(faust3,0,out,0);
AudioConnection patchCord1(faust3,0,out,1);

float hue;

void setup() {
    AudioMemory(2);
    audioShield.enable();
    audioShield.volume(1.5);
    Serial.begin(9600);

    faust3.setParamValue("ctgain", .4);
    faust3.setParamValue("gain1", .2);

    hue = 90;
}

void loop() {
    if (Serial.available() > 0){
        hue = Serial.parseFloat();
        if(hue != 0.0){
        Serial.println(hue);
        faust3.setParamValue("hue", hue);
    }
    }
    delay(50);
}