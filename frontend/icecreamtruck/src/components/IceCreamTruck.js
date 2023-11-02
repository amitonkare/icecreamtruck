'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Form, Button, Alert } from 'react-bootstrap';

const IceCreamTruck = () => {
  const [truck, setTruck] = useState({});
  const [selectedCheckboxes, setSelectedCheckboxes] = useState({});
  const [selectedQuantities, setSelectedQuantities] = useState({});
  const [showSuccessAlert, setShowSuccessAlert] = useState(false);
  const [showErrorAlert, setShowErrorAlert] = useState(false);
  const [totalPrice, setTotalPrice] = useState(null);
  const [showTodaysCollection, setShowTodaysCollection] = useState(false);
  const [todaysCollection, setTodaysCollection] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setSelectedCheckboxes({ ...selectedCheckboxes, [name]: checked });
  };

  const handleQuantityChange = (e) => {
    const { name, value } = e.target;
    setSelectedQuantities({ ...selectedQuantities, [name]: value });
  }

  useEffect(() => {
    axios.get(`${process.env.NEXT_PUBLIC_API_URL}/truck/1/details/`)
      .then(response => {
        setTruck(response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      truck: truck.id,
      items: []
    };
    const foodItems = Object.keys(selectedCheckboxes);
    if (foodItems.length === 0) {
      setErrorMessage('No items selected');
      setShowErrorAlert(true)
      setTimeout(() => {
        setShowErrorAlert(false);
      }, 5000)
      return;
    }
    for (let i = 0; i < foodItems.length; i += 1) {
      payload['items'].push({ food_item_flavour: foodItems[i], quantity: selectedQuantities[foodItems[i]] });
    }
    axios.post(`${process.env.NEXT_PUBLIC_API_URL}/order/buy_food/`, payload)
      .then(response => {
        setShowSuccessAlert(true);
        setTimeout(() => {
          setShowSuccessAlert(false);
          setTotalPrice(0);
        }, 5000)
        setTotalPrice(response.data.total_price);
        setSelectedCheckboxes({});
        setSelectedQuantities({});
      })
      .catch(error => {
        if (error.response.status == 422) {
          setErrorMessage('Sorry! Insufficient Inventory.');
        } else {
          setErrorMessage(error.response.data.detail);
        }
        setShowErrorAlert(true);
        setTimeout(() => {
          setShowErrorAlert(false);
        }, 5000)
        console.error('Error buying food data:', error);
      });
  }

  const getTotalCollection = () => {
    axios.get(`${process.env.NEXT_PUBLIC_API_URL}/order/todays_collection/`)
      .then(response => {
        setTodaysCollection(response.data.total_collection || 0);
        setShowTodaysCollection(true);
      })
      .catch(error => {
        console.error('Error buying food data:', error);
      });
  }

  return (
    <div className="row">
      <div className='w-50 m-auto'>
        <Alert show={showSuccessAlert} variant="success" transition onClose={() => setShowSuccessAlert(false)} dismissible>Enjoy! Your order is taken and the order amount is ${totalPrice}</Alert>
        <Alert show={showErrorAlert} variant="danger" transition onClose={() => setShowErrorAlert(false)} dismissible>{errorMessage}</Alert>
        <Alert show={showTodaysCollection} variant="info" transition onClose={() => setShowTodaysCollection(false)} dismissible>Todays collection is: ${todaysCollection}</Alert>
      </div>
      <h2 className="text-3xl text-center my-3 text-bold" style={{ height: "40px" }}>Ice-Cream Truck</h2>
      <div className="mx-auto w-50 px-5">
        {truck?.id && <>
          <div className='row border-top border-bottom align-items-center justify-content-between py-2'>
            <div className='col-4'>
              <h4 className="h-8 text-xl mt-2 mb-0 font-bold">
                {truck.name}<br />
              </h4>
              <small>
                Location: {truck.address}
              </small>
            </div>
            <div className='col-4 text-end'>
              <Button type="button" variant='info' onClick={getTotalCollection}>Collection Today</Button>
            </div>
          </div>
          <Form onSubmit={handleSubmit}>
            <div className='row align-items-center justify-content-center border-bottom mb-3 py-2'>
              <div className="col-6 w-50 h4 mb-0">Menu</div>
              <div className="col-6 text-end">
                <Button type="submit" variant='success' size="md">Order</Button>
              </div>
            </div>
            <ul className='border-bottom px-4'>
              {truck.items.map(item => (
                <li key={item.food_item_flavour} className='mb-2' style={{ listStyleType: "none" }}>
                  <Form.Check
                    key={item.food_item_flavour}
                    type="checkbox"
                    name={item.food_item}
                  >
                    <div className='row align-items-center justify-content-center' style={{ width: "100%" }}>
                      <div className='col-md-8'>
                        <Form.Check.Input type="checkbox" name={item.food_item_flavour} checked={selectedCheckboxes[item.food_item_flavour] || false} onChange={handleCheckboxChange} style={{ fontSize: "20px", marginRight: "10px", marginTop: "0px" }} />
                        <Form.Check.Label htmlFor="food_item" className='ml-2'>{item.food_item}, Flavour: {item.flavour}
                          <br /><small className="text-center">Available Quantity: {item.quantity}</small>
                        </Form.Check.Label>
                      </div>
                      <div className='col-md-4 row justify-content-end'>
                        <Form.Control type="text" placeholder="Quantity" name={item.food_item_flavour} onChange={handleQuantityChange} style={{ maxWidth: "100px" }} />
                      </div>
                    </div>
                    <br />
                  </Form.Check>
                </li>
              ))}
            </ul>
          </Form>
        </>
        }
      </div>
    </div>
  );
};

export default IceCreamTruck;
