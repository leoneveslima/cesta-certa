package com.mylist.compras;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;

import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Edge-to-edge (Android 15+): empurra o app para baixo da barra de status
        // e mantém a cor de fundo do tema escuro atrás dela.
        getWindow().getDecorView().setBackgroundColor(Color.parseColor("#0F172A"));
        View content = findViewById(android.R.id.content);
        content.setBackgroundColor(Color.parseColor("#1E293B"));
        ViewCompat.setOnApplyWindowInsetsListener(content, (v, insets) -> {
            Insets bars = insets.getInsets(WindowInsetsCompat.Type.statusBars()
                    | WindowInsetsCompat.Type.displayCutout());
            v.setPadding(0, bars.top, 0, 0);
            return insets;
        });
        ViewCompat.requestApplyInsets(content);
    }
}
