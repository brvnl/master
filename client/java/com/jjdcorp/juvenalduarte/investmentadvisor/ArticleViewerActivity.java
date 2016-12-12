package com.jjdcorp.juvenalduarte.investmentadvisor;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.design.widget.CollapsingToolbarLayout;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.webkit.WebView;
import android.widget.TextView;

import java.util.Set;

public class ArticleViewerActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_article_viewer);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        WebView textView = (WebView) findViewById(R.id.textViewFulltext);
        Intent intent = getIntent();
        int index = intent.getIntExtra("article_index", 0);
        Article current = ServerData.getInstance().getArticle(index);

        CollapsingToolbarLayout ctb= (CollapsingToolbarLayout)findViewById(R.id.toolbar_layout);
        ctb.setTitle(current.title);
        String full = current.text + "\n\n" + current.url;

        String htmlText = NewsViewer1Activity.txtToHtml(full);
        textView.loadDataWithBaseURL(null, htmlText, "text/html", "utf-8", null);

        //SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
        //boolean silent = settings.getBoolean("silentMode", false);

    }
}
