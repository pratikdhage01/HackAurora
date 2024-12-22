import { View, Text, Pressable, StyleSheet, ImageBackground } from 'react-native';
import React, { useState } from 'react';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

type ButtonName = 
  | "Add Money"
  | "Withdraw Money"
  | "Pay Money"
  | "Analyse Spendings"
  | "Financial Advice"
  | "Pay Bills";

const Manual = () => {
  const [hoveredButton, setHoveredButton] = useState<ButtonName | null>(null);
  const router = useRouter(); // Hook to navigate between screens

  const handleNavigation = (label: ButtonName) => {
    console.log(label); // Logs button label
    if (label === "Add Money") {
      router.push("/addmoney"); // Navigate to the 'addmoney' page
    } else if (label === "Withdraw Money") {
      router.push("/withdrawmoney"); // Navigate to the 'withdrawmoney' page
    } else if (label === "Pay Money") {
      router.push("/paymoney"); // Navigate to the 'paymoney' page
    } else {
      router.push("/details"); // Navigate to the 'details' page for other actions
    }
  };

  return (
    <ImageBackground
      source={require('/Users/devbhangale/Code/hack/app2/assets/images/bg.jpeg')} // Path to the background image
      style={styles.background}
    >
      <View className="p-4">
        {/* Balance Card */}
        <View className="bg-white p-6 rounded-lg shadow-lg mb-4 w-full max-w-sm ml-4">
          <Text className="text-xl font-bold">Your Balance</Text>
          <Text className="text-2xl font-semibold mt-2">₹2000</Text>
        </View>

        {/* Add and Withdraw Money Buttons */}
        <View className="flex-row justify-between w-full max-w-sm ml-4 mt-2">
          {[
            { label: "Add Money", icon: "add-circle-outline" },
            { label: "Withdraw Money", icon: "remove-circle-outline" },
          ].map(({ label, icon }, index) => (
            <Pressable
              key={index}
              onPress={() => handleNavigation(label as ButtonName)}
              onPressIn={() => setHoveredButton(label as ButtonName)}
              onPressOut={() => setHoveredButton(null)}
              style={{
                backgroundColor: hoveredButton === label ? "slategray" : "black",
                paddingVertical: 10,
                paddingHorizontal: 20,
                borderRadius: 25,
                flex: 1,
                marginHorizontal: index === 0 ? 0 : 10,
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <Ionicons name={icon as "add-circle-outline" | "remove-circle-outline"} size={36} color="white" />
              <Text style={{ color: "white", fontWeight: "bold", marginTop: 5 }}>{label}</Text>
            </Pressable>
          ))}
        </View>

        {/* Additional Actions Card */}
        <View className="mb-4 mt-4 w-full max-w-sm ml-4">
          <View className="flex-row justify-between">
            {[
              { label: "Analyse Spendings", icon: "search-outline" },
              { label: "Financial Advice", icon: "cash-outline" },
              { label: "Pay Bills", icon: "receipt-outline" },
            ].map(({ label, icon }, index) => (
              <Pressable
                key={index}
                onPress={() => handleNavigation(label as ButtonName)}
                onPressIn={() => setHoveredButton(label as ButtonName)}
                onPressOut={() => setHoveredButton(null)}
                style={{
                  backgroundColor: hoveredButton === label ? "slategray" : "black",
                  paddingVertical: 10,
                  paddingHorizontal: 10,
                  borderRadius: 25,
                  flex: 1,
                  marginHorizontal: 10,
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <Ionicons
                  name={icon as "search-outline" | "cash-outline" | "receipt-outline"}
                  size={24}
                  color={"white"}
                />
                <Text
                  className='text-center'
                  style={{
                    color: "white",
                    fontWeight: "bold",
                    fontSize: 12,
                  }}
                >
                  {label}
                </Text>
              </Pressable>
            ))}
          </View>
        </View>

        {/* Pay Money Button */}
        <View className="mt-80 mb-4 w-full max-w-sm ml-4">
          <View className="flex-row justify-between">
            {[
              { label: "Pay Money", icon: "send-outline", color: "red" },
            ].map(({ label, icon, color }, index) => (
              <Pressable
                key={index}
                onPress={() => handleNavigation(label as ButtonName)}
                onPressIn={() => setHoveredButton(label as ButtonName)}
                onPressOut={() => setHoveredButton(null)}
                style={{
                  backgroundColor: hoveredButton === label ? "slategray" : "white",
                  borderWidth: hoveredButton === label ? 0 : 1,
                  borderColor: "black",
                  paddingVertical: 10,
                  paddingHorizontal: 10,
                  borderRadius: 25,
                  flex: 1,
                  marginHorizontal: index === 0 ? 0 : 10,
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <Ionicons name={icon as "send-outline"} size={36} color={color} />
                <Text
                  style={{
                    color: "black",
                    fontWeight: "bold",
                    fontSize: 12,
                  }}
                >
                  {label}
                </Text>
              </Pressable>
            ))}
          </View>
        </View>
      </View>
    </ImageBackground>
  );
};

const styles = StyleSheet.create({
  background: {
    flex: 1, // Ensures the background image covers the full screen
    width: '100%',
    height: '100%',
  },
});

export default Manual;
