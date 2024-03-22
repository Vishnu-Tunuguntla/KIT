import React from "react";
import {createBottomTabNavigator} from "@react-navigation/bottom-tabs"

import InventoryPage from "./InventoryPage"
import ProcessingAndQueriesPage from "./ProcessingAndQueriesPage";
import UploadVideoPage from "./UploadVideo"



const Tab = createBottomTabNavigator();

const Tabs = () => {
    return(
        <Tab.Navigator>
            <Tab.Screen name = "UploadVideo" component = {UploadVideoPage}/>
            <Tab.Screen name = "ProcessingAndQueries" component = {ProcessingAndQueriesPage}/>
            <Tab.Screen name = "Inventory" component = {InventoryPage}/>
        </Tab.Navigator>
    )
}
export default Tabs