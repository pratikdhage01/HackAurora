import React, { useState } from 'react';
import { View, Text, TouchableOpacity, FlatList, StyleSheet, Alert, ImageBackground, Linking } from 'react-native';
import * as Speech from 'expo-speech';
import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';

type Message = {
  text: string;
  sender: 'user' | 'server';
};

export default function VoiceChat() {
  const [isListening, setIsListening] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);

  const handleVoiceRecognition = async () => {
    if (isListening) {
      setIsListening(false);
      if (recording) {
        await recording.stopAndUnloadAsync();
        console.log('Recording stopped');
        sendAudioToBackend();
      }
      return;
    }

    setIsListening(true);

    const { status } = await Audio.requestPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Denied', 'Cannot access microphone');
      return;
    }

    try {
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording: newRecording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(newRecording);
      await newRecording.startAsync();
      console.log("Recording started");
    } catch (error) {
      console.error("Error starting recording:", error);
      Alert.alert('Error', 'Failed to start recording');
      setIsListening(false);
    }
  };

  const sendAudioToBackend = async () => {
    if (!recording) return;

    try {
      const uri = recording.getURI();
      if (!uri) throw new Error('No valid audio URI available');

      const audioData = await FileSystem.readAsStringAsync(uri, {
        encoding: FileSystem.EncodingType.Base64,
      });

      const response = await fetch("http://localhost:3000", { 
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ audio: audioData }),
      });

      if (!response.ok) throw new Error("Failed to send audio");

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        { text: data.reply, sender: 'server' },
      ]);

      Speech.speak(data.reply);

      if (data.reply.toLowerCase().includes("paying bill")) {
        speakAndRedirect();
      }
    } catch (error) {
      console.error("Error sending audio to backend:", error);
      Alert.alert("Error", "Failed to send audio to the backend.");
    }
  };

  const speakAndRedirect = () => {
    const message = "You will have to enter your consumer number and captcha to pay the electricity bill.";
    Speech.speak(message, {
      onDone: () => {
        const url = "https://wss.mahadiscom.in/wss/wss?uiActionName=getViewPayBill";
        Linking.canOpenURL(url)
          .then((supported) => {
            if (supported) {
              Linking.openURL(url);
            } else {
              Alert.alert("Error", "URL not supported");
            }
          })
          .catch((err) => console.error("Error checking URL:", err));
      },
    });
  };

  return (
    <ImageBackground
      source={require('/Users/devbhangale/Code/hack/app2/assets/images/bg.jpeg')}
      style={styles.background}
    >
      <View style={styles.container}>
        <FlatList
          data={messages}
          keyExtractor={(_, index) => index.toString()}
          renderItem={({ item }) => (
            <View
              style={[
                styles.messageContainer,
                item.sender === 'user' ? styles.userMessage : styles.serverMessage,
              ]}
            >
              <Text style={styles.messageText}>{item.text}</Text>
            </View>
          )}
        />
        <TouchableOpacity style={styles.button} onPress={handleVoiceRecognition}>
          <Text style={styles.buttonText}>
            {isListening ? "Stop Recording" : "Start Recording"}
          </Text>
        </TouchableOpacity>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  background: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  messageContainer: {
    padding: 10,
    borderRadius: 5,
    marginVertical: 5,
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#d1e7dd',
  },
  serverMessage: {
    alignSelf: 'flex-start',
    backgroundColor: 'black',
  },
  messageText: {
    fontSize: 16,
    color: 'white',
  },
  button: {
    backgroundColor: '#007bff',
    padding: 15,
    alignItems: 'center',
    borderRadius: 5,
    marginTop: 10,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
