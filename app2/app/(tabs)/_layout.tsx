import {
  createMaterialTopTabNavigator,
  MaterialTopTabNavigationEventMap,
  MaterialTopTabNavigationOptions
} from '@react-navigation/material-top-tabs'
import React from 'react'
import { withLayoutContext } from 'expo-router';
import { ParamListBase, TabNavigationState } from '@react-navigation/native';

const { Navigator } = createMaterialTopTabNavigator();

export const MaterialTopTabs = withLayoutContext<
  MaterialTopTabNavigationOptions,
  typeof Navigator,
  TabNavigationState<ParamListBase>,
  MaterialTopTabNavigationEventMap
>(Navigator);

const Layout = () => {
  return (
    <MaterialTopTabs
      screenOptions={{
        swipeEnabled: false, // Disable swipe functionality
      }}
    >
      <MaterialTopTabs.Screen name="index" options={{ title: "Voice" }} />
      <MaterialTopTabs.Screen name="explore" options={{ title: "Manual" }} />
    </MaterialTopTabs>
  );
};

export default Layout;