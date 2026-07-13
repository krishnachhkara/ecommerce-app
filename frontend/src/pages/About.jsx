import React from 'react'
import Title from '../components/Title.jsx'
import { assets } from '../assets/assets.js'
import NewsLetterBox from '../components/NewsLetterBox.jsx'

const About = () => {


  return (
    <div>
      <div className='text-2xl text-center pt-8 border-t '>
        <Title text1={'ABOUT'} text2={"US"} />
      </div>
      <div className='my-10 flex flex-col md:flex-row gap-16'>
        <img src={assets.about_img} className='w-full md:max-w-112.5' alt="" />
        <div className='flex flex-col justify-center gap-6 md:w-2/4 text-gray-600'>
          <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Minima voluptatum minus praesentium assumenda a sequi, illo cupiditate quod dicta maiores reprehenderit ipsum recusandae consequatur officiis molestiae odit sed quisquam vel corporis maxime?</p>
          <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Cumque aliquam, quibusdam molestias corporis quae totam unde inventore saepe ipsa laboriosam commodi eaque. Sed voluptate eius vitae debitis rem! Sed, accusantium.</p>
          <b className='text-gray-800'>Our Mission</b>
          <p>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laboriosam a temporibus magnam consequatur commodi ullam dignissimos, similique quibusdam sint quo voluptatum blanditiis dolorum sequi, id dicta veniam, voluptas voluptates mollitia?</p>

        </div>


      </div>
      <div className='text-xl py-4'>
        <Title text1={"WHY"} text2={"CHOOSE US"}/>
      </div>
      <div className='flex flex-col md:flex-row text-sm mb-20'>
        <div className='border px-10 md:px-16 py-8 sm:py-20 flex flex-col gap-5'>
          <b>Quality Assurance:</b>
          <p className='text-gray-600'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus adipisci et, aliquid enim magni maiores ab nemo optio eos ipsum animi, dignissimos libero alias, hic a. Facere adipisci ab aperiam!</p>
        </div>
        <div className='border px-10 md:px-16 py-8 sm:py-20 flex flex-col gap-5'>
          <b>Convenience:</b>
          <p className='text-gray-600'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus adipisci et, aliquid enim magni maiores ab nemo optio eos ipsum animi, dignissimos libero alias, hic a. Facere adipisci ab aperiam!</p>
        </div>
        <div className='border px-10 md:px-16 py-8 sm:py-20 flex flex-col gap-5'>
          <b>Exceptional Customer Serivce</b>
          <p className='text-gray-600'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus adipisci et, aliquid enim magni maiores ab nemo optio eos ipsum animi, dignissimos libero alias, hic a. Facere adipisci ab aperiam!</p>
        </div>

      </div>
      <NewsLetterBox/>
      
    </div>
  )
}

export default About
