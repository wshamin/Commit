import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UsersPage() {
  const [users, setUsers] = useState([]);
  const [page, setPage] = useState(1);
  const [editing, setEditing] = useState(null);
  const [updatedFields, setUpdatedFields] = useState({});

  useEffect(() => {
    async function fetchUsers() {
      try {
        const headers = {
          'Authorization': `Bearer ${localStorage.getItem("accessToken")}`,
        };
        const response = await axios.get(`${process.env.REACT_APP_API_URL}users/?page=${page}`, { headers });
        setUsers(response.data);
      } catch (error) {
        console.error("Ошибка при получении пользователей:", error);
      }
    }
    fetchUsers();
  }, [page]);

  const deleteUser = async (id) => {
    try {
      const headers = {
        'Authorization': `Bearer ${localStorage.getItem("accessToken")}`,
      };
      const response = await axios.delete(`${process.env.REACT_APP_API_URL}users/${id}`, { headers });
      setUsers(users.filter(user => user._id !== id));
      if (response.status === 204) {
        alert("Пользователь удален");
      }
    } catch (error) {
      console.error("Ошибка при удалении пользователя:", error);
    }
  };

  const startEditing = (id) => {
    setEditing(id);
    setUpdatedFields({});
  };

  const handleChange = (event) => {
    setUpdatedFields({ ...updatedFields, [event.target.name]: event.target.value });
  };

  const updateUser = async (id) => {
    try {
      const headers = {
        'Authorization': `Bearer ${localStorage.getItem("accessToken")}`,
      };
      const response = await axios.put(`${process.env.REACT_APP_API_URL}users/${id}`, updatedFields, { headers });
      setUsers(users.map(user => (user._id === id ? response.data : user)));
      setEditing(null);
    } catch (error) {
      console.error("Ошибка при обновлении пользователя:", error);
    }
  };

  return (
    <div>
      <h2>Список пользователей</h2>
      <ul>
        {users.map(user => (
          <li key={user._id}>
            {user.email}
            {editing === user._id ? (
              <>
                <br /><input name="name" placeholder="Имя" onChange={handleChange} /><br />
                <input name="email" placeholder="Почта" onChange={handleChange} /><br />
                <input name="password" placeholder="Пароль" onChange={handleChange} /><br />
                <input name="role" placeholder="Роль" onChange={handleChange} /><br />
                <button onClick={() => updateUser(user._id)}>Сохранить</button>
              </>
            ) : (
              <button onClick={() => startEditing(user._id)} style={{ marginLeft: '10px' }}>Редактировать</button>
            )}
            <button onClick={() => deleteUser(user._id)} style={{ marginLeft: '10px' }}>Удалить</button>
          </li>
        ))}
      </ul>
      <button onClick={() => setPage(page - 1)}>Предыдущая страница</button>
      <button onClick={() => setPage(page + 1)}>Следующая страница</button>
    </div>
  );
}

export default UsersPage;
