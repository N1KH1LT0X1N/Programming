import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function TodoList() {
  const [todos, setTodos] = useState([]);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [newTodoDescription, setNewTodoDescription] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }
      const response = await axios.get('http://localhost:8000/todos/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setTodos(response.data);
    } catch (error) {
      console.error('Error fetching todos', error);
      if (error.response && error.response.status === 401) {
        navigate('/login');
      }
    }
  };

  const addTodo = async (event) => {
    event.preventDefault();
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:8000/users/me/todos/', 
        { title: newTodoTitle, description: newTodoDescription },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      setNewTodoTitle('');
      setNewTodoDescription('');
      fetchTodos();
    } catch (error) {
      console.error('Error adding todo', error);
      alert('Failed to add todo!');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Your Todos</h2>
        <button onClick={handleLogout} className="btn btn-danger">Logout</button>
      </div>
      
      <form onSubmit={addTodo} className="mb-4">
        <div className="mb-3">
          <input 
            type="text" 
            className="form-control" 
            placeholder="New Todo Title" 
            value={newTodoTitle} 
            onChange={(e) => setNewTodoTitle(e.target.value)} 
            required 
          />
        </div>
        <div className="mb-3">
          <textarea 
            className="form-control" 
            placeholder="Description (optional)" 
            value={newTodoDescription} 
            onChange={(e) => setNewTodoDescription(e.target.value)} 
          ></textarea>
        </div>
        <button type="submit" className="btn btn-success">Add Todo</button>
      </form>

      <ul className="list-group">
        {todos.map((todo) => (
          <li key={todo.id} className="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <h5>{todo.title}</h5>
              {todo.description && <p className="mb-0">{todo.description}</p>}
            </div>
            {/* Add complete/delete functionality here later */}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TodoList;
