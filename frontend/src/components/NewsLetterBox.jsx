import React from 'react'

const NewsLetterBox = () => {

    const onSubmitHandler = (e) => {
        e.preventDefault();
        
    }

  return (
      <div className='text-center'>
          <p className='text-2xl font-medium text-gray-800y'>
              Subscribe now & get 20% off
          </p>
          <p className='text-gray-400 mt-3'>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Fugiat nihil beatae aspernatur fuga ducimus et.
              
          </p>
          <form onSubmit={onSubmitHandler} className='w-full sm:w-1/2 flex items-center gap-3 mx-auto my-6 border pl-3 ' >
              <input className='w-full sm:flex-1 outline-none' type="email" placeholder='Enter your e-mail' required />
              <button type='submit' className='bg-black text-white text-s px-10 py-4'>SUBSCRIBE</button>
          </form>
      
    </div>
  )
}

export default NewsLetterBox;
