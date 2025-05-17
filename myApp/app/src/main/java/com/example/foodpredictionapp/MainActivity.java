package com.example.foodpredictionapp;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import java.io.IOException;
import java.io.InputStream;

public class MainActivity extends AppCompatActivity {
    private static final int PICK_IMAGE_REQUEST = 1;
    private Uri imageUri;
    private ImageView imageView;
    private TextView txtResponse;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button btnSelect = findViewById(R.id.btnSelectImage);
        imageView = findViewById(R.id.imageView);
        txtResponse = findViewById(R.id.txtResponse);

        btnSelect.setOnClickListener(v -> chooseImage());
    }

    private void chooseImage() {
        Intent intent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        startActivityForResult(intent, PICK_IMAGE_REQUEST);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == PICK_IMAGE_REQUEST && resultCode == RESULT_OK && data != null) {
            imageUri = data.getData();
            imageView.setImageURI(imageUri);
            uploadImage();
        }
    }

    private void uploadImage() {
        try {
            InputStream inputStream = getContentResolver().openInputStream(imageUri);
            byte[] imageBytes = new byte[inputStream.available()];
            inputStream.read(imageBytes);

            MultipartBody.Part body = MultipartBody.Part.createFormData(
                    "image",
                    "upload.jpg",
                    RequestBody.create(imageBytes, MediaType.parse("image/*"))
            );

            OkHttpClient client = new OkHttpClient();
            Request request = new Request.Builder()
                    .url("http://192.168.50.138:5000//predict")
                    .post(new MultipartBody.Builder()
                            .setType(MultipartBody.FORM)
                            .addFormDataPart("image", "upload.jpg",
                                    RequestBody.create(imageBytes, MediaType.parse("image/jpeg")))
                            .build())
                    .build();

            client.newCall(request).enqueue(new Callback() {
                @Override public void onFailure(Call call, IOException e) {
                    runOnUiThread(() -> txtResponse.setText("Lỗi: " + e.getMessage()));
                }

                @Override public void onResponse(Call call, Response response) throws IOException {
                    String res = response.body().string();
                     // format JSON
//                    try {
//                        String decoded = null;
//                        decoded = new JSONObject(res).toString(4);
//                        String finalDecoded = decoded;
//                        runOnUiThread(() -> txtResponse.setText(finalDecoded));
//                    } catch (JSONException e) {
//                        throw new RuntimeException(e);
//                    }

                        try{
                            System.out.println("vào đây được");
                            JSONObject json = new JSONObject(res);
                            double confidence = json.getDouble("confidence");
                            JSONObject foodInfo = json.getJSONObject("food_info");
                            String name = foodInfo.getString("name");
                            String description = foodInfo.getString("description");

                            JSONArray ingredients = foodInfo.getJSONArray("ingredients");
                            JSONArray instructions = foodInfo.getJSONArray("instructions");

                            StringBuilder result = new StringBuilder();
                            result.append("Tên món ăn dự đoán: ").append(name).append("\n\n");
                            result.append("Độ tin cậy: ").append(confidence).append("\n\n");
                            result.append("Mô tả món ăn:\n").append(description).append("\n\n");
                            result.append("Nguyên liệu:\n");
                            for (int i = 0; i < ingredients.length(); i++) {
                                result.append("• ").append(ingredients.getString(i)).append("\n");
                            }
                            result.append("\nCách nấu:\n\n");
                            for (int i = 0; i < instructions.length(); i++) {
                                result.append("• ").append(instructions.getString(i)).append("\n\n");
                            }
                            runOnUiThread(() -> txtResponse.setText(result.toString()));
                        }catch (Exception e){
                            runOnUiThread(() ->txtResponse.setText("Lỗi đọc:"+e.getMessage()));
                        }

                }
            });

        } catch (Exception e) {
            txtResponse.setText("Lỗi xử lý ảnh: " + e.getMessage());
        }
    }
}

