import { View, Text, TextInput, Pressable, Alert } from 'react-native';
import React, { useState } from 'react';

const AddMoney = () => {
  const [amount, setAmount] = useState<string>(''); // State to hold the input amount

  const handleAddMoney = () => {
    if (!amount || isNaN(Number(amount)) || Number(amount) <= 0) {
      Alert.alert('Invalid Amount', 'Please enter a valid amount to add.');
    } else {
      Alert.alert('Success', `₹${amount} has been added to your wallet.`);
      setAmount(''); // Clear the input after adding money
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 16 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 16 }}>Add Money</Text>
      
      {/* Input Box */}
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
      
      {/* Add Money Button */}
      <Pressable
        onPress={handleAddMoney}
        style={{
          backgroundColor: 'black',
          paddingVertical: 12,
          paddingHorizontal: 24,
          borderRadius: 8,
        }}
      >
        <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 16 }}>Add Money</Text>
      </Pressable>
    </View>
  );
};

export default AddMoney;
