int led[5] = {12, 11, 10, 9, 8};
int count;


void setup()
{
  for (int i = 0; i < 5; i++)
  {
    pinMode(led[i], OUTPUT);
  }
  
  Serial.begin(115200);
}

void loop()
{
  if (Serial.available() > 0)
  {
    count = Serial.parseInt();

    if (count < 0) count = 0;
    if (count > 5) count = 5;

    for (int i = 0; i < 5; i++) 
    {
      digitalWrite(led[i], i < count ? HIGH : LOW);
    }
  }
}