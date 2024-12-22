import { View, Text, TextInput, Pressable, Alert } from 'react-native';
import React, { useState } from 'react';

const PayMoney = () => {
  const [amount, setAmount] = useState<string>(''); // State to hold the input amount
  const [recipient, setRecipient] = useState<string>(''); // State to hold the recipient's mobile number

  const handlePayMoney = () => {
    // Validate the inputs
    if (!amount || isNaN(Number(amount)) || Number(amount) <= 0) {
      Alert.alert('Invalid Amount', 'Please enter a valid amount to pay.');
      return;
    }
    if (!recipient || recipient.length !== 10 || isNaN(Number(recipient))) {
      Alert.alert('Invalid Recipient', 'Please enter a valid 10-digit mobile number.');
      return;
    }

    // Process the payment (this can be extended with actual payment logic)
    Alert.alert('Payment Success', `₹${amount} has been paid to ${recipient}.`);
    setAmount(''); // Clear the amount input
    setRecipient(''); // Clear the recipient input
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 16 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 16 }}>Pay Money</Text>
      
      {/* Amount Input */}
      <TextInput
        value={amount}
        onChangeText={setAmount}
        placeholder="Enter Amount"
        keyboardType="numeric"
        style={{
          width: '80%',
          padding: 12,
          borderWidth: 1,
          borderColor: '#ccc',
          borderRadius: 8,
          marginBottom: 16,
          fontSize: 16,
        }}
      />
      
      {/* Recipient Mobile Number Input */}
      <TextInput
        value={recipient}
        onChangeText={setRecipient}
        placeholder="Enter Recipient's Mobile Number"
        keyboardType="numeric"
        maxLength={10}
        style={{
          width: '80%',
          padding: 12,
          borderWidth: 1,
          borderColor: '#ccc',
          borderRadius: 8,
          marginBottom: 16,
          fontSize: 16,
        }}
      />
      
      {/* Pay Money Button */}
      <Pressable
        onPress={handlePayMoney}
        style={{
          backgroundColor: 'black',
          paddingVertical: 12,
          paddingHorizontal: 24,
          borderRadius: 8,
        }}
      >
        <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 16 }}>Pay Money</Text>
      </Pressable>
    </View>
  );
};

export default PayMoney;
