import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import {
  Container,
  TextField,
  Button,
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  IconButton,
} from "@mui/material";
import { Autocomplete } from "@mui/lab";
import axios from "axios";
import { Author } from "../../interfaces/Author";
import { Buyer } from "../../interfaces/Buyer";
import { Publisher } from "../../interfaces/Publisher";
import { BASE_URL } from "../../constants";
import { Link, useNavigate, useParams } from "react-router-dom";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

interface MagazineForm {
  title: string;
  number_of_pages: number;
  publish_date: string;
  quantity: number;
  ibn: number;
  price: number;
  author: string;
  publisher: string;
  buyers: string[];
}

const MagazineAdd = () => {
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<MagazineForm>({
    defaultValues: {
      title: "",
      number_of_pages: 0,
      publish_date: "",
      ibn: 0,
      price: 0,
      quantity: 0,
      author: "",
      publisher: "",
      buyers: [],
    },
  });
  const [buyers, setBuyers] = useState<Buyer[]>([]);
  const [authors, setAuthors] = useState<Author[]>([]);
  const [publishers, setPublishers] = useState<Publisher[]>([]);
  const [loadingData, setLoadingData] = useState(true);
  const [loadingMagazine, setLoadingMagazine] = useState(true);
  const { magazineId } = useParams();
  const isEditMode = magazineId !== undefined;

  const navigate = useNavigate();

  // Fetch buyers, authors, and publishers data
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch authors, publishers, and buyers
        const [authorsResponse, publishersResponse, buyersResponse] =
          await Promise.all([
            axios.get(`${BASE_URL}/authors/list`),
            axios.get(`${BASE_URL}/publishers/list`),
            axios.get(`${BASE_URL}/buyers/list`),
          ]);

        setAuthors(authorsResponse.data);
        setPublishers(publishersResponse.data);
        setBuyers(buyersResponse.data);
        console.log(authorsResponse.data)
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoadingData(false);
      }
    };

    fetchData();
  }, []);

  // Fetch existing magazine data if in edit mode
  useEffect(() => {
    const fetchMagazine = async () => {
      setLoadingMagazine(true);
      try {
        const response = await axios.get(`${BASE_URL}/magazines/${magazineId}`);
        const magazineData = response.data;
        setValue("title", magazineData.title);
        setValue("number_of_pages", magazineData.number_of_pages);
        setValue("publish_date", magazineData.publish_date);
        setValue("ibn", magazineData.ibn);
        setValue("price", magazineData.price);
        setValue("quantity", magazineData.quantity);
        setValue("author", magazineData.author.id);
        setValue("publisher", magazineData.publisher.id);
        setValue(
          "buyers",
          magazineData.buyers.map((buyer: any) => buyer.id)
        );
      } catch (error) {
        console.error("Error fetching magazine data:", error);
      } finally {
        setLoadingMagazine(false);
      }
    };

    if (magazineId) {
      fetchMagazine();
    }
  }, [magazineId, setValue]);

  const onSubmit = async (data: MagazineForm) => {
    try {
      if (magazineId) {
        console.log(data);

        await axios.put(`${BASE_URL}/magazines/${magazineId}/`, data);
        console.log(data);
        alert("Magazine successfully updated!");
      } else {
        await axios.post(`${BASE_URL}/magazines/`, data);
        alert("Magazine successfully added!");
      }
      navigate("/magazines");
    } catch (error) {
      console.error("Error adding/updating magazine:", error);
      alert("Failed to add/update magazine.");
    }
  };

  if (loadingData) {
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
    <Container maxWidth="sm" sx={{ marginBottom: "2rem" }}>
      <Box sx={{ margin:4  }}>
      <IconButton component={Link} sx={{ mr: 3 }} to={`/magazines/${magazineId}/details`}>
            <ArrowBackIcon />
          </IconButton>
        <Typography variant="h4" align="center">
          {magazineId ? "Update Magazine" : "Add Magazine"}
        </Typography>
        <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 3 }}>
          <TextField
            label="Title"
            fullWidth
            {...register("title", { required: true })}
            sx={{ mt: 2 }}
          />

          <TextField
            label="Number of Pages"
            fullWidth
            type="number"
            {...register("number_of_pages", {
              required: true,
              min: 1,
              max: 1000,
            })}
            sx={{ mt: 2 }}
          />

          <TextField
            label="Publish Date"
            fullWidth
            type="date"
            InputLabelProps={{ shrink: true }}
            {...register("publish_date", { required: true })}
            sx={{ mt: 2 }}
          />

          <TextField
            label="IBN"
            fullWidth
            type="number"
            {...register("ibn", { required: true })}
            sx={{ mt: 2 }}
          />

          <TextField
            label="Price"
            fullWidth
            type="number"
            {...register("price", { required: true })}
            sx={{ mt: 2 }}
          />

          <TextField
            label="Quantity"
            fullWidth
            type="number"
            {...register("quantity", { required: true })}
            sx={{ mt: 2 }}
          />
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel id="author-label">Author</InputLabel>
            <Select
              labelId="author-label"
              {...register("author", { required: true })}
              label="Author"
            >
              {authors.map((author) => (
                <MenuItem key={author.id} value={author.id}>
                  {author.first_name} {author.last_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel id="publisher-label">Publisher</InputLabel>
            <Select
              labelId="publisher-label"
              {...register("publisher", { required: true })}
              label="Publisher"
            >
              {publishers.map((publisher) => (
                <MenuItem key={publisher.id} value={publisher.id}>
                  {publisher.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Autocomplete
            multiple
            options={buyers}
            getOptionLabel={(option) => `${option.id}: ${option.name}`}
            fullWidth
            sx={{ mt: 2 }}
            onChange={(_, value) =>
              setValue(
                "buyers",
                value.map((buyer) => buyer.id.toString())
              )
            }
            renderInput={(params) => (
              <TextField
                {...params}
                label="Buyers"
                placeholder="Select Buyers"
              />
            )}
          />

          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            sx={{ my: 3 }}
          >
            {magazineId ? "Update Magazine" : "Add Magazine"}{" "}
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default MagazineAdd;
