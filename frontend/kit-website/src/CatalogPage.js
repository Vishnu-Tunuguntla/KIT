import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Grid } from '@mui/material';

function CatalogPage() {
  // Dummy product data - replace with real data as needed
  const products = [
    { id: 1, name: 'Product 1' },
    { id: 2, name: 'Product 2' },
    { id: 3, name: 'Product 3' },
    // Add more products as needed
  ];

  return (
    <Grid container spacing={3} style={{ padding: '20px', paddingTop: '100px' }}> {/* Increased top padding */}
      {products.map((product) => (
        <Grid item xs={12} sm={6} md={4} key={product.id}>
          <Card>
            <CardMedia
              component="img"
              height="140"
              image="/static/images/cards/placeholder.png"
              alt="Image placeholder"
            />
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                {product.name}
              </Typography>
              {/* You can add more content here, such as description or price */}
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}

export default CatalogPage;
