import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './pages/login';
import Cadastro from './pages/Cadastro'; // Importe o componente Cadastro

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="container mt-5">
          <h1>Bem-vindo ao Sistema de Cadastro</h1>
          <p className="lead">Faça seu cadastro ou login para continuar</p>
          <div className="mt-4">
            {/* Substitua <a> por <Link> e href por to */}
            <Link to="/cadastro" className="btn btn-primary me-2">Cadastro</Link>
            <Link to="/login" className="btn btn-secondary">Login</Link>
          </div>
        </div>

        {/* Defina suas rotas */}
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />
        </Routes>
      </div>
    </Router>
  );
}

