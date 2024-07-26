import HeaderComp from '../components/HeaderComp.tsx';

import { Outlet } from 'react-router-dom';
const HomeLayout = () => {
  return (
    <>
    <div>
        <HeaderComp/>
            <Outlet/>
        </div>
    </>
      )
}

export default HomeLayout