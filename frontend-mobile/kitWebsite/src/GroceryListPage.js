import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, Alert } from 'react-native';
import { AntDesign } from '@expo/vector-icons'; // Import AntDesign for the bell icon

const GroceryListPage = () => {
  const [groceryItem, setGroceryItem] = useState('');
  const [groceryList, setGroceryList] = useState([]);

  const handleAddItem = () => {
    if (groceryItem.trim() === '') {
      Alert.alert('Error', 'Please enter an item.');
      return;
    }
    const newItem = { name: groceryItem, reminderSet: false }; // Adjusted to include reminder status
    setGroceryList((currentList) => [...currentList, newItem]);
    setGroceryItem(''); // Reset the input field after adding
  };

  const handleRemoveItem = (indexToRemove) => {
    setGroceryList((currentList) => currentList.filter((_, index) => index !== indexToRemove));
  };

  // New function to toggle reminder status
  const toggleReminder = (index) => {
    setGroceryList((currentList) =>
      currentList.map((item, i) =>
        i === index ? { ...item, reminderSet: !item.reminderSet } : item
      )
    );
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.header}>Grocery List</Text>
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Enter grocery item..."
          value={groceryItem}
          onChangeText={setGroceryItem}
        />
        <TouchableOpacity style={styles.addButton} onPress={handleAddItem}>
          <Text style={styles.buttonText}>Add</Text>
        </TouchableOpacity>
      </View>
      {groceryList.map((item, index) => (
        <View key={index} style={styles.item}>
          <Text style={styles.itemText}>{item.name}</Text>
          <TouchableOpacity onPress={() => toggleReminder(index)}>
            <AntDesign name="bells" size={24} color={item.reminderSet ? "black" : "#D3D3D3"} /> 
          </TouchableOpacity>
          <TouchableOpacity onPress={() => handleRemoveItem(index)}>
            <Text style={styles.removeButtonText}>X</Text>
          </TouchableOpacity>
        </View>
      ))}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    paddingTop: 50,
    paddingHorizontal: 20,
    backgroundColor: '#ffffff', // A light background color for the whole page
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
    textAlign: 'center',
  },
  inputContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  input: {
    flex: 1,
    marginRight: 10,
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 15,
    paddingVertical: 10,
    borderRadius: 8,
    fontSize: 16,
  },
  addButton: {
    backgroundColor: '#0066cc',
    padding: 10,
    borderRadius: 20,
    justifyContent: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
  },
  item: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#f0f0f0',
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderRadius: 8,
    marginBottom: 10,
  },
  itemText: {
    fontSize: 16,
  },
  removeButtonText: {
    fontSize: 16,
    color: 'red',
  },
});

export default GroceryListPage;
