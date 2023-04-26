import { useEffect, useState } from "react";
import {
  Box,
  Button,
  CircularProgress,
  Container,
  IconButton,
  InputLabel,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import { Magazine } from "../../interfaces/Magazine";
import { BASE_URL } from "../../constants";
import { Link } from "react-router-dom";
import { Add, DeleteForever, Edit, ReadMore } from "@mui/icons-material";

const MagazinesPage = () => {
  const [loading, setLoading] = useState(false);
  const [magazines, setMagazines] = useState<Magazine[]>();
  const [minPages, setMinPages] = useState<number>();

  const fetchMagazines = () => {
    setLoading(true);
    fetch(`${BASE_URL}/magazines/list/`)
      .then((response) => response.json())
      .then((data) => {
        setMagazines(data);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchMagazines();
  }, []);

  
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMinPages(parseInt(event.target.value));
  };

  const handleFilter = () => {
    if (!minPages || minPages === 0) {
      fetchMagazines();
    } else if (minPages > 0) {
      setLoading(true);
      fetch(`${BASE_URL}/magazines/above/${minPages}/`)
        .then((response) => response.json())
        .then((data) => {
          setMagazines(data);
          setLoading(false);
        });
    }
  };

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


  return (
    <Container maxWidth="xl">
      <Box mt={4} mb={2}>
        <Typography variant="h4" component="h1">
          Magazines List
        </Typography>
      </Box>
      {!loading && (
        <IconButton component={Link} sx={{ mr: 3 }} to={`/magazines/add`}>
          <Tooltip title="Add a new magazine" arrow>
            <Add color="primary" />
          </Tooltip>
        </IconButton>
      )}
      <Box mb={2} display="flex" alignItems="center" gap="1rem" justifyContent="right">
        <InputLabel htmlFor="min-pages">Magazines with pages above</InputLabel>
        <TextField
          id="min-pages"
          type="number"
          value={minPages}
          onChange={handleChange}
        />
        <Button
          onClick={handleFilter}
          variant="contained"
          color="primary"
          sx={{ ml: 2 }}
        >
          Filter
        </Button>
      </Box>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell align="right">#</TableCell>
              <TableCell align="right">Title</TableCell>
              <TableCell align="right">Price</TableCell>
              <TableCell align="right">Pages</TableCell>
              <TableCell align="right">Quantity</TableCell>
              <TableCell align="right">Operations</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {magazines &&
              magazines.map((magazine, idx) => {
                return (
                  <TableRow key={idx}>
                    <TableCell align="right">{idx + 1}</TableCell>
                    <TableCell align="right">{magazine.title}</TableCell>
                    <TableCell align="right">{magazine.price}</TableCell>
                    <TableCell align="right">{magazine.number_of_pages}</TableCell>
                    <TableCell align="right">{magazine.quantity}</TableCell>
                    <TableCell align="right">
                      <IconButton
                        component={Link}
                        sx={{ mr: 3 }}
                        to={`/magazines/${magazine.id}/details`}
                      >
                        <Tooltip title="View course details" arrow>
                          <ReadMore color="primary" />
                        </Tooltip>
                      </IconButton>

                      <IconButton
                        component={Link}
                        sx={{ mr: 3 }}
                        to={`/magazines/${magazine.id}/edit`}
                      >
                        <Edit />
                      </IconButton>

                      <IconButton
                        component={Link}
                        to={`/magazines/${magazine.id}/delete`}
                      >
                        <DeleteForever sx={{ color: "red" }} />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default MagazinesPage;
