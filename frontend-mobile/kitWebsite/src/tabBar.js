import React from "react";
import {createBottomTabNavigator} from "@react-navigation/bottom-tabs"

import InventoryPage from "./InventoryPage"
import ProcessingAndQueriesPage from "./ProcessingAndQueriesPage";
import UploadVideoPage from "./UploadVideo"
import GroceryListPage from "./GroceryListPage";



const Tab = createBottomTabNavigator();

const Tabs = () => {
    return(
        <Tab.Navigator>
            <Tab.Screen name = "Grocery List" component={GroceryListPage}/>
            <Tab.Screen name = "Upload" component = {UploadVideoPage}/>
            <Tab.Screen name = "Query" component = {ProcessingAndQueriesPage}/>
            <Tab.Screen name = "Inventory" component = {InventoryPage}/>
        </Tab.Navigator>
    )
}
export default Tabs