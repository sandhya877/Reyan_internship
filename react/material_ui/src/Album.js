import * as React from 'react';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Modal from '@mui/material/Modal';
import InputAdornment from '@mui/material/InputAdornment';
import { useReducer, useEffect } from 'react';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import ButtonGroup from '@mui/material/ButtonGroup';
import TextField from '@mui/material/TextField';
import SearchIcon from '@mui/icons-material/Search';
import EditIcon from '@mui/icons-material/Edit';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

function Copyright() {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const defaultTheme = createTheme();

export default function Album() {
  const [openDeleteModal, setOpenDeleteModal] = React.useState(false);
  const [openUpdateModal, setOpenUpdateModal] = React.useState(false);
  const [openAddModal, setOpenAddModal] = React.useState(false);
  const [updateTask, setUpdateTask] = React.useState(null);
  const [newTask, setNewTask] = React.useState({
    text: '',
    title: '',
    img: '',
  });
  
  const API_BASE_URL = 'http://127.0.0.1:8000/items';
  const handleUpdateAction = (task) => {
    setUpdateTask(task);
    setOpenUpdateModal(true);
  };
 /*
  const handleUpdateTask = () => {
    // Dispatch an action to update the task in the reducer state
    dispatch({ type: 'changed', task: updateTask });
    setOpenUpdateModal(false);
  };
 
*/
  const handleAddAction = (task) => {
    setNewTask(task);
    setOpenAddModal(true);
  };
  
  const handleCloseDeleteModal = () => {
    setOpenDeleteModal(false);
  };

  const handleCloseUpdateModal = () => {
    setOpenUpdateModal(false);
  };

  const handleCloseAddModal = () => {
    setOpenAddModal(false);
  };

  /*

  const handleDeleteAction = (task) => {
    // Set the task to delete
    setUpdateTask(task);
    // Open the delete modal
    setOpenDeleteModal(true);
  };
  */

  
  const handleUpdateTask = async () => {
    try {
      if (!updateTask || !updateTask._id || updateTask._id === undefined) {
        throw new Error('Invalid updateTask object or missing _id.$oid property.');
      }
      console.log(updateTask.title,updateTask.link)
      const response = await fetch(`${API_BASE_URL}/${updateTask._id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          _id:updateTask._id,
          link: updateTask.link,
          title: updateTask.title,
          img: updateTask.img,
        }),
      });
      console.log(response)
      if (response.ok) {
        // Item updated successfully
        console.log('Item updated successfully');
      } else {
        // Handle the case where the item update fails
        console.error('Failed to update item. Status:', response.status);
      }
    } catch (error) {
      console.error('Error updating item:', error);
    } finally {
      // Close the update modal regardless of success or failure
      setOpenUpdateModal(false);
    }
  };
  
  
  
/*
  const handleDeleteTask = async () => {
    try {
      if (!updateTask || !updateTask._id || updateTask._id.$oid === undefined) {
        throw new Error('Invalid updateTask object or missing _id.$oid property.');
      }
      const taskToDelete = tasks.find((t) => t._id === updateTask._id);
      if (!taskToDelete) {
        throw new Error(`Task with id ${updateTask._id} not found.`);
      }
      const response = await fetch(`${API_BASE_URL}/${updateTask._id}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        console.log(updateTask.title)
        throw new Error(`Failed to delete task. Status: ${response.status}`);
      }
      dispatch({ type: 'deleted', id: updateTask._id});
      setOpenDeleteModal(false);
    } catch (error) {
      console.log(updateTask.title)
      console.error('Error deleting task:', error.message);
    }
  };
  

  const handleDeleteAction = async (task) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/items/${task._id}`, {
        method: 'DELETE',
      });
  
      if (response.ok) {
        // Item deleted successfully
        console.log('Item deleted successfully');
      } else {
        // Handle the case where the item deletion fails
        console.error('Failed to delete item. Status:', response.status);
      }
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  */
  function generateRandomHexString(length) {
    const characters = '0123456789abcdef';
    let result = '';
  
    for (let i = 0; i < length; i++) {
      const randomIndex = Math.floor(Math.random() * characters.length);
      result += characters[randomIndex];
    }
  
    return result;
  }
  
  
  const handleDeleteAction = (task) => {
    // Set the task to delete
    setUpdateTask(task);
    // Open the delete modal
    setOpenDeleteModal(true);
  };
  
  const handleDeleteTask = async () => {
    try {
      if (!updateTask || !updateTask._id || updateTask._id === undefined) {
        throw new Error('Invalid updateTask object or missing _id.$oid property.');
      }
  
      const response = await fetch(`${API_BASE_URL}/${updateTask._id}`, {
        method: 'DELETE',
      });
  
      if (response.ok) {
        // Item deleted successfully
        console.log('Item deleted successfully');
      } else {
        // Handle the case where the item deletion fails
        console.error('Failed to delete item. Status:', response.status);
      }
    } catch (error) {
      console.error('Error deleting item:', error);
    } finally {
      // Close the delete modal regardless of success or failure
      setOpenDeleteModal(false);
    }
  };
  
  const handleAddTask = async () => {
    try {
      

     
      const response = await fetch(`${API_BASE_URL}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          link: newTask.link,
          title: newTask.title,
          img: newTask.img,
        }),
      });
      console.log(response.ok)
      if (response.ok) {
        // Item updated successfully
        console.log('Item added successfully');
      } else {
        // Handle the case where the item update fails
        console.error('Failed to update item. Status:', response.status);
      }
    } catch (error) {
      console.error('Error updating item:', error);
    } finally {
      // Close the update modal regardless of success or failure
      setOpenUpdateModal(false);
    }
  };
  

  
  
  React.useEffect(() => {
    if (openDeleteModal) {
      // Handle any logic you need when the delete modal is opened
    }
  }, [openDeleteModal]);

  React.useEffect(() => {
    if (openUpdateModal) {
      // Handle any logic you need when the update modal is opened
    }
  }, [openUpdateModal]);

  React.useEffect(() => {
    if (openAddModal) {
      // Handle any logic you need when the add modal is opened
    }
  }, [openAddModal]);

  function tasksReducer(tasks, action) {
    console.log("Reducer Action:", action);
    switch (action.type) {
      case 'initialize': {
        return action.tasks;
      }
      case 'added': {
        const newTaskId = tasks.length + 1;
      
        return [...tasks, { _id: { $oid: newTaskId.toString() }, text: action.text, title: action.title, img: action.img }];
      }
      
      case 'changed': {
        return tasks.map((t) => (t.id === action.task.id ? action.task : t));
      }
      case 'deleted': {
        return tasks.filter((t) => t._id.$oid !== action.id);
      }
      default: {
        throw Error('Unknown action: ' + action.type);
      }
    }
  }
 
  const initialTasks = [];
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);

  useEffect(() => {
    
  
   
  const fetchInitialTasks = async () => {
    try {
      const response = await fetch(API_BASE_URL, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    
      if (!response.ok) {
        throw new Error(`Failed to fetch tasks. Status: ${response.status}`);
      }
  
      const responseData = await response.json();

      if (Array.isArray(responseData)) {
        // Extract the array from the 'data' property
        const initialTasks = responseData;
        console.log('Fetched tasks:', initialTasks);
        dispatch({ type: 'initialize', tasks: initialTasks });
      } else {
        console.log('Fetched tasks:', initialTasks);
        throw new Error('Fetched data is not an array.');
      }
    } catch (error) {
      console.error('Error fetching initial tasks:', error);
    }
  };
  fetchInitialTasks();
}, []);
  


  return (
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />

      <main>
        <Box
          sx={{
            bgcolor: 'background.paper',
            pt: 8,
            pb: 6,

          }}
        >
          <Container maxWidth="sm">
            <Typography
              component="h2"
              variant="h3"
              align="center"
              color="text.primary"
              gutterBottom
            >
              Amazon Moderator Page
            </Typography>
            
            <Stack
              sx={{ pt: 4 }}
              direction="row"
              spacing={2}
              justifyContent="center"
            >
              <>
              <Box

      sx={{
        display: 'flex',
        alignItems: 'center', // Align items at the center vertically
        padding: '8px',
        width:'90%',
        // Optional: Add padding for better visual appeal
      }}
      noValidate
      autoComplete="off"
    >
      <TextField
        id="outlined-basic"
        placeholder="search an item"
        variant="outlined"
        sx={{ flex: 1, height: '50px',width:"100%" ,borderRadius: '10px', marginRight: '20px' }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <IconButton>
                <SearchIcon />
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
      <button onClick={handleAddAction} style={{ height: '51px', borderRadius: '10px' }}>
        Add
      </button>
    </Box>
              </>
            </Stack>
          </Container>
        </Box>
        <Container sx={{ py: 8 }} maxWidth="md">
          <Grid container spacing={4}>
            {tasks.map((task, index) => (
              <Grid item key={index} xs={12} sm={6} md={4}>
                <Card
                  sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                >
                  <CardMedia
                    component="div"
                    sx={{
                      pt: '56.25%',
                    }}
                    image={task.img}
                  />
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography gutterBottom variant="h5" component="h2">
                      {task.title}
                    </Typography>
                    <Typography>
                      {task.title}
                    </Typography>
                  </CardContent>
                  <CardActions sx={{ justifyContent: 'center' }}>
                    <IconButton aria-label="edit" onClick={() => handleUpdateAction(task)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton aria-label="delete" onClick={() => handleDeleteAction(task)}>
                      <DeleteIcon />
                    </IconButton>
                  


                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </main>
      <Box sx={{ bgcolor: 'background.paper', p: 6 }} component="footer">
        <Typography variant="h6" align="center" gutterBottom>
          Footer
        </Typography>
        <Typography
          variant="subtitle1"
          align="center"
          color="text.secondary"
          component="p"
        >
          Something here to give the footer a purpose!
        </Typography>
        <Copyright />
      </Box>

      {/* Modal for delete action */}
      <Modal
        open={openDeleteModal}
        onClose={handleCloseDeleteModal}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography id="modal-modal-description" sx={{ mt: 2 }}>
            Are you sure you want to delete this?
          </Typography>
          <br>
          </br>
          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            

              <Button onClick={handleDeleteTask}>Yes</Button>
              <Button onClick={handleCloseDeleteModal}>No</Button>
            
          </div>
        </Box>
      </Modal>

      {/* Modal for update action */}
      <Modal
        open={openUpdateModal}
        onClose={handleCloseUpdateModal}
        aria-labelledby="modal-update-title"
        aria-describedby="modal-update-description"
      >
        <Box sx={style}>
          <Typography id="modal-update-title" variant="h6" component="h2">
            Update Content
          </Typography>
          <div style={{ mt: 2 }}>
            {/* Input field for updating the task text */}
            <TextField
              label="Task link"
              value={updateTask ? updateTask.link : ''}
              onChange={(e) => setUpdateTask({ ...updateTask, link: e.target.value })}
              fullWidth
              margin="normal"
            />
            {/* Input field for updating other task properties (e.g., title, img) */}
            <TextField
              label="Task Title"
              value={updateTask ? updateTask.title : ''}
              onChange={(e) => setUpdateTask({ ...updateTask, title: e.target.value })}
              fullWidth
              margin="normal"
            />
            <TextField
              label="Task Image URL"
              value={updateTask ? updateTask.img : ''}
              onChange={(e) => setUpdateTask({ ...updateTask, img: e.target.value })}
              fullWidth
              margin="normal"
            />
          </div>
          <br>
          </br>

          <div style={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
            
              {/* Call handleUpdateTask when the "Update" button is clicked */}
              <Button onClick={handleUpdateTask}>Update</Button>
              <Button onClick={handleCloseUpdateModal}>Cancel</Button>

          </div>
        </Box>
      </Modal>

      {/* Modal for add action */}
      <Modal
        open={openAddModal}
        onClose={handleCloseAddModal}
        aria-labelledby="modal-add-title"
        aria-describedby="modal-add-description"
      >
        <Box sx={style}>
          
          <div style={{ mt: 2 }}>
            <TextField
                label="Task Text"
                value={newTask.link}
                onChange={(e) => setNewTask({ ...newTask, link: e.target.value })}
                fullWidth
                margin="normal"
              />
              <TextField
                label="Task Title"
                value={newTask.title}
                onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                fullWidth
                margin="normal"
              />
              <TextField
                label="Task Image URL"
                value={newTask.img}
                onChange={(e) => setNewTask({ ...newTask, img: e.target.value })}
                fullWidth
                margin="normal"
              />
          </div>
          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            
            
                {/* Call handleAddTask when the "Add" button is clicked */}
                <Button onClick={handleAddTask}>Add</Button>
                <Button onClick={handleCloseAddModal}>Cancel</Button>
              

          </div>
        </Box>
      </Modal>
    </ThemeProvider>
  );
}
