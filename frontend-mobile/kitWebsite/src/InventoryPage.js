import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, ScrollView, StyleSheet, Alert } from 'react-native';
import axios from 'axios';

function InventoryPage() {
  const [foodItems, setFoodItems] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [userRequest, setUserRequest] = useState('');
  const [gptResponse, setGptResponse] = useState('');

  useEffect(() => {
    fetchFoodItems();
  }, []);

  const fetchFoodItems = async () => {
    try {
      const response = await axios.get('http://34.233.181.229:5000/api/food-items');
      setFoodItems(response.data);
    } catch (error) {
      console.error('Error fetching food items:', error);
      Alert.alert('Error', 'Error fetching food items');
    }
  };

  const handleInputChange = (name, value) => {
    if (!selectedItem || !selectedItem.Details) return;
    const [category, field] = name.split('.');
    const updatedDetails = { ...selectedItem.Details };
    if (category === 'nutrition_facts') {
      updatedDetails.nutrition_facts = {
        ...updatedDetails.nutrition_facts,
        [field]: value,
      };
    } else {
      updatedDetails[category] = value;
    }
    setSelectedItem({ ...selectedItem, Details: updatedDetails });
  };

  const handleSaveChanges = async () => {
    if (!selectedItem) {
      Alert.alert("Error", "No item selected for saving changes.");
      return;
    }
    try {
      await axios.put(`http://34.233.181.229:5000/api/food-items/${selectedItem.ItemID}`, selectedItem);
      Alert.alert("Success", "Changes saved successfully");
      fetchFoodItems(); // Refetch the food items after saving changes
    } catch (error) {
      console.error('Error saving changes:', error);
      Alert.alert("Error", "Error saving changes. Please try again.");
    }
  };

  const handleSendRequest = async () => {
    if (!userRequest.trim()) {
      Alert.alert("Error", "The request input is empty.");
      return;
    }
    try {
      const response = await axios.post('http://34.233.181.229:5000/api/gpt-request', { request: userRequest });
      setGptResponse(response.data.answer);
      setUserRequest(''); // Clear the request input field after sending
      Alert.alert("Success", "Request sent successfully");
    } catch (error) {
      console.error('Error sending GPT request:', error);
      Alert.alert("Error", "Error sending GPT request. Please try again.");
    }
  };

  return (
    <ScrollView style={styles.container}>
      {foodItems.map((item) => (
        <View key={item.ItemID} style={styles.item} onTouchEnd={() => setSelectedItem(item)}>
          <Text style={styles.itemText}>{item.Details.brand} - {item.Details.name}</Text>
        </View>
      ))}
      {selectedItem && (
        <View style={styles.detailsTable}>
          <TextInput
            style={styles.input}
            onChangeText={(value) => handleInputChange('name', value)}
            value={selectedItem?.Details?.name || ''}
            placeholder="Name"
          />
          {/* Add additional TextInput components for other fields as needed */}
          <Button title="Save" onPress={handleSaveChanges} />
        </View>
      )}
      <View style={styles.helperBox}>
        <TextInput
          style={styles.textArea}
          onChangeText={setUserRequest}
          value={userRequest}
          placeholder="Type your request here..."
          multiline={true}
          numberOfLines={4}
        />
        <Button title="Send Request" onPress={handleSendRequest} />
        {gptResponse && <Text style={styles.gptResponse}>{gptResponse}</Text>}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#ffffff', // A light background color for the whole page
  },
  item: {
    backgroundColor: '#f0f0f0', // A subtle color for each food item entry
    borderRadius: 10, // Rounded corners for food items
    paddingVertical: 15,
    paddingHorizontal: 20,
    marginVertical: 8,
    flexDirection: 'row', // For layout flexibility
    justifyContent: 'space-between', // Space out elements within each item
    alignItems: 'center', // Align items vertically
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
    elevation: 3, // Elevation for shadow (Android)
  },
  itemText: {
    fontSize: 16, // A readable text size
    color: '#333', // A color that ensures good readability
    fontFamily: 'System', // Default system font. You can change this to any custom font you have set up
  },
  detailsTable: {
    marginTop: 20, // Space from the item list to the details section
  },
  input: {
    backgroundColor: '#ffffff', // White background for input fields for contrast and focus
    borderWidth: 1,
    borderColor: '#cccccc', // Subtle border color
    borderRadius: 8, // Consistent rounded corners like the items
    padding: 10,
    fontSize: 16,
    color: '#000', // Black color for input text for readability
    marginBottom: 12, // Margin between input fields
  },
  helperBox: {
    marginTop: 30, // Space above the GPT request section
  },
  textArea: {
    backgroundColor: '#ffffff', // Matching the input fields for consistency
    borderWidth: 1,
    borderColor: '#cccccc', // Light border color
    borderRadius: 8, // Rounded corners for the text area
    padding: 10, // Padding inside the text area
    fontSize: 16, // Text size similar to inputs for consistency
    color: '#000', // Ensuring readability of the text
    height: 150, // Giving enough space for the user to type a request
    textAlignVertical: 'top', // Align text to start from the top in the text area
    marginBottom: 20, // Space below the text area before the button or response
  },
  gptResponse: {
    backgroundColor: '#eef2f5', // A very light background color for the response area to differentiate it
    borderRadius: 8, // Rounded corners for the response box
    padding: 15, // Padding inside the response box
    fontSize: 16, // Readable text size
    color: '#333', // Darker text for contrast and readability
    marginVertical: 20, // Margin above and below the response box
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
    elevation: 3, // Shadow to lift the response box slightly
  },
});

export default InventoryPage