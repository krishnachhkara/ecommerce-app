import React, { useContext, useEffect, useState } from 'react'
import { ShopContext } from '../context/ShopContext.jsx'
import { assets } from '../assets/assets.js';
import Title from '../components/Title.jsx';
import ProductItem from '../components/ProductItem.jsx';

const Collection = () => {

  const { products, search , showSearch } = useContext(ShopContext);
  const [showFilter, setShowFilter] = useState(false);
  const [filterProducts, setFilterProducts] = useState([]);
  const [category, setCategory] = useState([]);
  const [subCategory, setSubCategory] = useState([]);
  const [sortType, setSortType] = useState('relevant')

  // Toggle category selection:
  // If category exists → remove it
  // If category doesn't exist → add it
  const toggleCategory = (e) => {
    if (category.includes(e.target.value)) {
      setCategory(prev=> prev.filter(item=> item !== e.target.value))//removes when clicked again
    } else {
      setCategory(prev=> [...prev,e.target.value])//adds values if not present
    }
  }


  // Toggle category selection:
  // If subcategory exists → remove it
  // If subcategory doesn't exist → add it
  const toggleSubCategory = (e) => {
    if (subCategory.includes(e.target.value)) {
      setSubCategory(prev=> prev.filter(item=> item !== e.target.value))
    }
    else {
      setSubCategory(prev=> [...prev,e.target.value])
    }
  }

  const applyFilter = () => {

    let productsCopy = products.slice();//creating duplicate product array.

    if (showSearch && search) {
      productsCopy = productsCopy.filter(item=> item.name.toLowerCase().includes(search.toLowerCase()))
    }

    if (category.length > 0) {
      productsCopy = productsCopy.filter(item=> category.includes(item.category))
    }
    if (subCategory.length > 0) {
      productsCopy = productsCopy.filter(item => subCategory.includes(item.subCategory))
    }

    setFilterProducts(productsCopy);// runs even if not filter is selected bcoz all the
    // above if will be false so the products copy will be passed as it is.
  }


  const sortProduct = () => {
    //creating copy of filterproducts to use filter with sort functions

    let filprodCopy = filterProducts.slice();

    switch (sortType) {
      // Sort products by price:
      // low-high  -> cheapest to expensive
      // high-low -> expensive to cheapest
      // Uses a copied array to avoid mutating state directly.
      case 'low-high':
        setFilterProducts(filprodCopy.sort((a, b) => (a.price - b.price)));
        // Put a before b if substracting output is -ve
        break;
      case 'high-low':
        setFilterProducts(filprodCopy.sort((a, b) => (b.price - a.price)));
        //Put b before a if substracting output is +ve
        break;
      default:
        applyFilter();
        break;
    }
  }


  useEffect(() => {
    applyFilter();

  }, [category, subCategory,search,showSearch])

  useEffect(() => {
    sortProduct();

  }, [sortType ])
  

  

  
  

  return (
    <div className='flex flex-col sm:flex-row gap-1 sm:gap-10 pt-10 border-t'>
      {/* Filter Options */}

      <div className='min-w-60'>
        <p onClick={() => setShowFilter(!showFilter)} className='my-2 text-xl flex items-center cursor-pointer gap-2'>FILTERS
          <img src={assets.dropdown_icon} className={`h-3 sm:hidden ${showFilter?'rotate-90':''}`} alt="" />
        </p>
        {/* Category Filter */}
        <div className={`border border-gray-300 pl-5 py-3 mt-6 ${showFilter ? '' : 'hidden'} sm:block`}>
          <p className='mb-3 text-sm font-medium'>CATEGORIES</p>
          <div className='flex flex-col gap-2 text-sm font-light text-gray-700'>
            <p className='flex gap-2'>
              <input type="checkbox" className='w-3' value={'Men'} onChange={toggleCategory} />Men

            </p>
            <p className='flex gap-2'>
              <input type="checkbox" className='w-3' value={'Women'} onChange={toggleCategory} />Women

            </p>
            <p className='flex gap-2'>
              <input type="checkbox" className='w-3' value={'Kids'} onChange={toggleCategory} />Kids

            </p>

          </div>
        </div>
        {/* Sub Catgeory Filter */}
        <div className={`border border-gray-300 pl-5 py-3 my-5 ${showFilter ? '' : 'hidden'} sm:block`}>
          <p className='mb-3 text-sm font-medium'>TYPE</p>
          <div className='flex flex-col gap-2 text-sm font-light text-gray-700'>
            <p className='flex gap-2'>
              <input type="checkbox" className='w-3' value={'Topwear'} onChange={toggleSubCategory} />Top-wear

            </p>
            <p className='flex gap-2'>
              <input type="checkbox" className='w-3' value={'Bottomwear'} onChange={toggleSubCategory} />Bottom-wear

            </p>
            <p className='flex gap-2'>
              <input type="checkbox" className='w-3' value={'Winterwear'} onChange={toggleSubCategory} />Winter-wear

            </p>

          </div>
        </div>

      </div>

      {/* Right Side */}

      <div className='flex-1'>
        <div className='flex justify-between text-base sm:text-2xl mb-4'>
          <Title text1={"ALL"} text2={"COLLECTION"} />
          {/* Product Sort */}
          <select onChange={(e)=>setSortType(e.target.value)} className='border border-gray-300 text-sm px-2'>
            <option value="relevant">Sort by: Relevant</option>
            <option value="low-high">Sort by: Price low-high</option>
            <option value="high-low">Sort by: Price high-low</option>

          </select>

        </div>
        {/* Map Products */}
        <div className='grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5 gap-y-6'>
          {
            filterProducts.map((item, index) => (
              <ProductItem key={index} id={item._id} name={item.name} image={item.image} price={item.price}/>
            ))
          }

        </div>

      </div>
      
    </div>
  )
}

export default Collection;
