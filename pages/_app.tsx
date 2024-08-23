import '../styles/global.css';
import { ThemeProvider } from 'next-themes'
import { useState, useContext } from 'react';
import { GlobalContext, GlobalContextValue } from '../contexts/globalContext';
import Modal from '../components/Modal';

export default function MyApp({ Component, pageProps }) {
  // const [globalContext, setGlobalContext] = useState < GlobalContextValue > {};

  const [globalContext, setGlobalContext] = useState<GlobalContextValue>({
    modalContent: null,
    isModalVisible: false,
  });

  return (
    <>
      <ThemeProvider forcedTheme="light">
      <GlobalContext.Provider
        value={{ value: globalContext, setValue: setGlobalContext }}>
        {globalContext.isModalVisible && <Modal />}
        <Component {...pageProps} />
      </GlobalContext.Provider>
      </ThemeProvider>
    </>
  );
}
