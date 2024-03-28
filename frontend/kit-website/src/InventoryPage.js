import React, { useState, useEffect } from 'react';
import axios from 'axios';

function InventoryPage() {

  const mockFoodItems = [
    { id: 1, Details: { name: 'Peanut Butter', brand: "Jiff's", ingredients: 'peanuts, sugar, salt' } },
    { id: 2, Details: { name: 'Jelly', brand: "Jam", ingredients: 'grapes, sugar, pectin' } },
    // Add more items as needed
  ];
  const [foodItems, setFoodItems] = useState(mockFoodItems);
  const [selectedItem, setSelectedItem] = useState(null);
  const [userRequest, setUserRequest] = useState('');
  const [gptResponse, setGptResponse] = useState('');
  const [recipeList, setRecipeList] = useState([]);
  const [recipe, setRecipe] = useState('');
  const [allergens, setAllergens] = useState([])



  useEffect(() => {
    fetchFoodItems();
  }, []);

  

  const fetchFoodItems = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/food-items');
      setFoodItems(response.data);
    } catch (error) {
      console.error('Error fetching food items:', error);
    }
  };

  const handleItemClick = (item) => {
    setSelectedItem(item);
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setSelectedItem((prevItem) => {
      const [category, field] = name.split('.');
      if (category === 'nutrition_facts') {
        return {
          ...prevItem,
          Details: {
            ...prevItem.Details,
            nutrition_facts: {
              ...prevItem.Details.nutrition_facts,
              [field]: value,
            },
          },
        };
      } else {
        return {
          ...prevItem,
          Details: {
            ...prevItem.Details,
            [category]: value,
          },
        };
      }
    });
  };

  const handleSaveChanges = async () => {
    try {
      await axios.put(`http://127.0.0.1:5000/api/food-items/${selectedItem.ItemID}`, selectedItem);
      console.log('Changes saved successfully');
      fetchFoodItems(); // Refetch the food items after saving changes
    } catch (error) {
      console.error('Error saving changes:', error);
    }
  };

  const handleUserRequestChange = (event) => {
    setUserRequest(event.target.value);
  };

  const handleSendRequest = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/gpt-request', { request: userRequest });
      setGptResponse(response.data.answer);
      setUserRequest('');
    } catch (error) {
      console.error('Error sending GPT request:', error);
      // Handle error response...
    }
  };

  const handleRecipeRequest = async () => {
    try {
      const recipeItemNames = recipeList.map(item => item.Details.name);
      
      const response = await axios.post('http://127.0.0.1:5000/api/recipe-request', { items: recipeItemNames });
      setRecipe(response.data.recipe); // Assuming the backend sends back a field named 'recipe'
      // Optionally clear the recipe list after getting the recipe
      setRecipeList([]);
    } catch (error) {
      console.error('Error sending recipe request:', error);
      // Optionally handle and display error to the user
    }
  };
  
  
  

  const removeFromRecipeList = (indexToRemove) => {
    setRecipeList((currentList) => currentList.filter((_, index) => index !== indexToRemove));
  };

  // ... (other component code)

const handleAddAllergen = (event) => {
  event.preventDefault();
  const allergen = event.target.allergen.value.trim();
  if (allergen && !allergens.includes(allergen)) {
    setAllergens(currentAllergens => [...currentAllergens, allergen]);
    event.target.allergen.value = ''; // Reset input after adding
  }
};

const addToRecipeList = (item) => {
  // Check for allergens in the item's ingredients
  const itemIngredients = item.Details.ingredients.toLowerCase();
  const containsAllergen = allergens.some(allergen => itemIngredients.includes(allergen.toLowerCase()));

  if (containsAllergen) {
    alert('Warning: May contain allergen!');
  } else {
    setRecipeList(currentList => [...currentList, item]);
  }
};

  return (
    <div className="inventory-page">
      <div className="scrollbar">
        {foodItems.map((item, index) => (
          <div key={index} className="food-item">
            <span onClick={() => handleItemClick(item)}>
              {item.Details.brand} - {item.Details.name}
            </span>
            <button onClick={(e) => {
              e.stopPropagation();
              addToRecipeList(item);
            }}>+</button>
          </div>
        ))}
      </div>
  
      {selectedItem && (
        <div className="details-table">
          <input
            type="text"
            name="name"
            value={selectedItem.Details.name || ''}
            onChange={handleInputChange}
            placeholder="Name"
          />
          <input
            type="text"
            name="brand"
            value={selectedItem.Details.brand || ''}
            onChange={handleInputChange}
            placeholder="Brand"
          />
          <input
            type="text"
            name="category"
            value={selectedItem.Details.category || ''}
            onChange={handleInputChange}
            placeholder="Category"
          />
          <input
            type="text"
            name="nutrition_facts.serving_size"
            value={selectedItem.Details.nutrition_facts?.serving_size || ''}
            onChange={handleInputChange}
            placeholder="Serving Size"
          />
          <input
            type="text"
            name="nutrition_facts.calories"
            value={selectedItem.Details.nutrition_facts?.calories || ''}
            onChange={handleInputChange}
            placeholder="Calories"
          />
          <input
            type="text"
            name="nutrition_facts.total_fat"
            value={selectedItem.Details.nutrition_facts?.total_fat || ''}
            onChange={handleInputChange}
            placeholder="Total Fat"
          />
          <input
            type="text"
            name="nutrition_facts.saturated_fat"
            value={selectedItem.Details.nutrition_facts?.saturated_fat || ''}
            onChange={handleInputChange}
            placeholder="Saturated Fat"
          />
          <input
            type="text"
            name="nutrition_facts.trans_fat"
            value={selectedItem.Details.nutrition_facts?.trans_fat || ''}
            onChange={handleInputChange}
            placeholder="Trans Fat"
          />
          <input
            type="text"
            name="nutrition_facts.cholesterol"
            value={selectedItem.Details.nutrition_facts?.cholesterol || ''}
            onChange={handleInputChange}
            placeholder="Cholesterol"
          />
          <input
            type="text"
            name="nutrition_facts.sodium"
            value={selectedItem.Details.nutrition_facts?.sodium || ''}
            onChange={handleInputChange}
            placeholder="Sodium"
          />
          <input
            type="text"
            name="nutrition_facts.total_carbohydrates"
            value={selectedItem.Details.nutrition_facts?.total_carbohydrates || ''}
            onChange={handleInputChange}
            placeholder="Total Carbohydrates"
          />
          <input
            type="text"
            name="nutrition_facts.dietary_fiber"
            value={selectedItem.Details.nutrition_facts?.dietary_fiber || ''}
            onChange={handleInputChange}
            placeholder="Dietary Fiber"
          />
          <input
            type="text"
            name="nutrition_facts.sugars"
            value={selectedItem.Details.nutrition_facts?.sugars || ''}
            onChange={handleInputChange}
            placeholder="Sugars"
          />
          <input
            type="text"
            name="nutrition_facts.protein"
            value={selectedItem.Details.nutrition_facts?.protein || ''}
            onChange={handleInputChange}
            placeholder="Protein"
          />
          <input
            type="text"
            name="ingredients"
            value={selectedItem.Details.ingredients || ''}
            onChange={handleInputChange}
            placeholder="Ingredients"
          />
          <input
            type="text"
            name="expiration_date"
            value={selectedItem.Details.expiration_date || ''}
            onChange={handleInputChange}
            placeholder="Expiration Date"
          />
          <input
            type="text"
            name="quantity"
            value={selectedItem.Details.quantity || ''}
            onChange={handleInputChange}
            placeholder="Quantity"
          />
          <button onClick={handleSaveChanges}>Save</button>
        </div>
      )}
    {/* Allergen Input Form */}
    <div className="allergen-section">
      <form onSubmit={handleAddAllergen} className="allergen-form">
        <input
          type="text"
          name="allergen"
          placeholder="Add allergen"
          className="allergen-input"
        />
        <button type="submit" className="allergen-submit">Add</button>
      </form>

      {/* Allergens List */}
      <div className="allergen-list">
        <h4>Allergens:</h4>
        <div className="allergen-items">
          {allergens.map((allergen, index) => (
            <span key={index} className="allergen-item">{allergen}</span>
          ))}
        </div>
      </div>
    </div>
    <div>
      <h4>Recipe List:</h4>
      {recipeList.map((item, index) => (
        <div key={index} className="food-item" style={{ justifyContent: 'space-between' }}>
          <span>{item.Details.name}</span>
          <button onClick={() => removeFromRecipeList(index)} style={{ marginLeft: '10px' }}>X</button>
        </div>
      ))}
      <button onClick={handleRecipeRequest}>Get Recipe</button>
      {recipe && (
        <div className="recipe-display">
          <h3>Recipe</h3>
          <p>{recipe}</p>
        </div>
      )}
    </div>

    <div className="helper-box">
      <textarea
        value={userRequest}
        onChange={handleUserRequestChange}
        placeholder="Type your request here..."
      ></textarea>
      <button onClick={handleSendRequest}>Send Request</button>
      {gptResponse && (
        <div className="gpt-response">
          <p>{gptResponse}</p>
        </div>
      )}
    </div>
  </div>
);
}

export default InventoryPage;