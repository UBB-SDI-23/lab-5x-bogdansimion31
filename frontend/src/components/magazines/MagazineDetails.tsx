import {
	Box,
	Button,
	Card,
	CardActions,
	CardContent,
	CircularProgress,
	IconButton,
	List,
	ListItem,
	ListItemText,
	Typography,
  } from "@mui/material";
  import { Container } from "@mui/system";
  import { useEffect, useState } from "react";
  import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
  import { BASE_URL } from "../../constants";
  import EditIcon from "@mui/icons-material/Edit";
  import DeleteForeverIcon from "@mui/icons-material/DeleteForever";
  import ArrowBackIcon from "@mui/icons-material/ArrowBack";
  import { Magazine } from "../../interfaces/Magazine";
  import axios, { AxiosError } from "axios";
  import UpgradeIcon from "@mui/icons-material/Upgrade";
  
  export const MagazineDetails = () => {
	const { magazineId } = useParams();
	const [magazine, setMagazine] = useState<Magazine>();
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const navigate = useNavigate();
	const location = useLocation();
	const isEditMode = location.pathname.includes("edit");
  
  
	useEffect(() => {
	  const fetchMagazine = async () => {
		setLoading(true);
		try {
		  const response = await axios.get(`${BASE_URL}/magazines/${magazineId}`);
		  setMagazine(response.data);
		} catch (err) {
		  if (axios.isAxiosError(err)) {
			setError(err.message);
		  } else {
			setError("An unknown error occurred.");
		  }
		} finally {
		  setLoading(false);
		}
	  };
	  fetchMagazine();
	}, [magazineId]);
  
	if (loading) {
	  return (
		<Box
		  display="flex"
		  justifyContent="center"
		  alignItems="center"
		  minHeight="100vh"
		>
		  <CircularProgress />
		</Box>
	  );
	}
  
	if (error) {
	  return (
		<Box
		  display="flex"
		  justifyContent="center"
		  alignItems="center"
		  minHeight="100vh"
		>
		  <Typography variant="h6" color="error">
			Error: {error}
		  </Typography>
		</Box>
	  );
	}
  
	return (
	  <Container>
		<Card>
		  <CardContent>
			<IconButton component={Link} sx={{ mr: 3 }} to={`/magazines`}>
			  <ArrowBackIcon />
			</IconButton>{" "}
			<Typography variant="h4">Magazine Details</Typography>
			<Typography>Magazine Title: {magazine?.title}</Typography>
			<Typography>Magazine Price: {magazine?.price}</Typography>
			<Typography>
			  Magazine Author First Name: {magazine?.author.first_name}
			</Typography>
			<Typography>
			  Magazine Author Last Name: {magazine?.author.last_name}
			</Typography>
			<Typography>Magazine Publisher Name: {magazine?.publisher.name}</Typography>
			<Typography>Magazine Buyers:</Typography>
			<List>
			  {magazine?.buyers?.map((buyer) => (
				<ListItem key={buyer.id} alignItems="center">
				  <ListItemText
					primary={buyer.name}
					primaryTypographyProps={{ align: "center" }}
				  />
				</ListItem>
			  ))}
			</List>
		  </CardContent>
		  <CardActions>
			<Box display="flex" justifyContent="center" width="100%">
			  <IconButton
				component={Link}
				sx={{ mr: 4 }}
				to={`/magazines/${magazineId}/edit`}
			  >
				<EditIcon />
			  </IconButton>
  
			  <IconButton
				component={Link}
				sx={{ mr: 3 }}
				to={`/magazines/${magazineId}/delete`}
			  >
				<DeleteForeverIcon sx={{ color: "red" }} />
			  </IconButton>
			</Box>
		  </CardActions>
		</Card>
	  </Container>
	);
  };
  