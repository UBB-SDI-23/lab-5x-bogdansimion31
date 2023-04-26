import { useState } from 'react'
import './App.css'
import { Route, Routes, BrowserRouter as Router } from 'react-router-dom'
import { AppMenu } from './components/AppMenu'
import MagazinesPage from './components/magazines/MagazinePage'
import { AppHome } from './components/AppHome'
import { MagazineDetails } from './components/magazines/MagazineDetails'
import MagazineAdd from './components/magazines/MagazineAdd'
import { MagazineDelete } from './components/magazines/MagazineDelete'
function App() {

  return (
    <div className="App">

      <Router>
        <AppMenu />

        <Routes>
          <Route path="/" element={<AppHome />} />
          <Route path="/magazines" element={<MagazinesPage />} />
          <Route path="/magazines/:magazineId/details" element={<MagazineDetails />} />
					<Route path="/magazines/:magazineId/edit" element={<MagazineAdd />} />
					<Route path="/magazines/add" element={< MagazineAdd/>} />
          <Route path="/magazines/:magazineId/delete" element={<MagazineDelete />} />

        </Routes>
      </Router>

    </div>
  )
}

export default App
