import { View, Text } from 'react-native';
import React from 'react';

const Details = () => {
  return (
    <View className="flex-1 justify-center items-center bg-white">
      <Text className="text-2xl font-bold">Details Page</Text>
      <Text className="mt-2 text-lg text-gray-600">
        Here is the detailed information about the selected action.
      </Text>
    </View>
  );
};

export default Details;
