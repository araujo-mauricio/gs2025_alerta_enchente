// Código para simulação de sensor de nível d’água com ESP32 (versão básica)

#define TRIG_PIN 5
#define ECHO_PIN 18
#define WIFI_SSID "SUA_REDE_WIFI"
#define WIFI_PASSWORD "SUA_SENHA"

#include <WiFi.h>
#include <HTTPClient.h>

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando-se ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
}

void loop() {
  long duracao;
  float distancia_cm;

  // Trigger do sensor ultrassônico
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duracao = pulseIn(ECHO_PIN, HIGH);
  distancia_cm = duracao * 0.034 / 2;

  Serial.print("Distância: ");
  Serial.print(distancia_cm);
  Serial.println(" cm");

  // Enviar os dados para o servidor local (ex: Flask ou FastAPI)
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("http://192.168.1.100:5000/nivel"); // IP do servidor local Python
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"nivel_cm\": " + String(distancia_cm) + "}";
    int httpResponseCode = http.POST(payload);

    Serial.print("Resposta HTTP: ");
    Serial.println(httpResponseCode);

    http.end();
  }

  delay(10000); // Aguarda 10 segundos antes da próxima leitura
}
