import React from 'react';
import { Text } from 'react-native'; // Import Text for header titles
import "@/global.css";
import { GluestackUIProvider } from "@/components/ui/gluestack-ui-provider";
import { Stack } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function RootLayout() {
  return (
    <GluestackUIProvider mode="light">
      <Stack>
        <Stack.Screen
          name="(tabs)"
          options={{
            headerLeft: () => <Ionicons name="person-outline" size={24} />,
            headerRight: () => <Ionicons name="settings-outline" size={24} />,
            headerTitle: () => <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Vollet</Text>, // Use a Text component
          }}
        />
        <Stack.Screen
          name="details"
          options={{
            headerTitle: () => <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Details</Text>, // Use a Text component
            headerBackTitle: "Back",
          }}
        />
        <Stack.Screen
          name="addmoney"
          options={{
            headerTitle: () => <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Add Money</Text>, // Use a Text component
            headerBackTitle: "Back",
          }}
        />
        <Stack.Screen
          name="withdrawmoney"
          options={{
            headerTitle: () => <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Withdraw Money</Text>, // Use a Text component
            headerBackTitle: "Back",
          }}
        />
        <Stack.Screen
          name="paymoney"
          options={{
            headerTitle: () => <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Pay Money</Text>, // Use a Text component
            headerBackTitle: "Back",
          }}
        />
      </Stack>
    </GluestackUIProvider>
  );
}
