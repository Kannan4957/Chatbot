import React from 'react';

const Heading = ({tittle}) => {
    return (
        <div className='bg-[#443627] flex justify-center items-center '>
            <h1 className='text-white  text-2xl md:text-3xl p-2'>{tittle}</h1>
        </div>
    );
}

export default Heading;
