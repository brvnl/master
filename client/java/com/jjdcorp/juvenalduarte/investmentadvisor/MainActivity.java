package com.jjdcorp.juvenalduarte.investmentadvisor;

import android.graphics.Color;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;


public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {
    public final static String EXTRA_MESSAGE = "com.example.myfirstapp.MESSAGE";
    public boolean loggedIn = false;
    TextView mkeywordsViewr;
    TextView mNkeywordsViewr;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        mkeywordsViewr = (TextView) findViewById(R.id.content_main_tv2);
        mNkeywordsViewr = (TextView) findViewById(R.id.content_main_tv3);
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onPrepareOptionsMenu(Menu menu) {
        TextView tv1 = (TextView) findViewById(R.id.textView);
        LoginStatusSingleton status = LoginStatusSingleton.getInstance();
        if (status.getStatus()) {
            tv1.setText(status.getCredentials().user);
            String kwordsStr = status.getKeywords();
            String[] keywords = kwordsStr.split("\\|", -1);

            try {
                mkeywordsViewr.setText("Positive Keywords: " + keywords[0]);
                mkeywordsViewr.setTextColor(Color.rgb(0, 0, 102)); // Dark Blue
            } catch (Exception e) {
            }

            try {
                mNkeywordsViewr.setText("Negative Keywords: " + keywords[1]);
                mNkeywordsViewr.setTextColor(Color.rgb(102,0,0)); // Dark Red
            } catch (Exception e) {
            }

        } else {
            tv1.setText("Not logged yet...");
        }

        return super.onPrepareOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            Intent intent = new Intent(this, SettingsActivity.class);
            this.startActivity(intent);
        }
        invalidateOptionsMenu();
        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.LogIn) {
            Intent intent = new Intent(this, LoginActivity.class);
            this.startActivity(intent);
        } else if (id == R.id.RetrieveNews) {
            LoginStatusSingleton logInStatus = LoginStatusSingleton.getInstance();
            if (logInStatus.getStatus()) {
                Intent intent = new Intent(this, NewsViewer1Activity.class);
                this.startActivity(intent);
            } else {
                Snackbar mySnackbar = Snackbar.make(findViewById(R.id.content_main), R.string.error_notLogged, Snackbar.LENGTH_LONG);
                mySnackbar.show();
            }
        } else if (id == R.id.SummaryView) {
            LoginStatusSingleton logInStatus = LoginStatusSingleton.getInstance();
            if (logInStatus.getStatus()) {
                Intent intent = new Intent(this, SumaryViewActivity.class);
                this.startActivity(intent);
            } else {
                Snackbar mySnackbar = Snackbar.make(findViewById(R.id.content_main), R.string.error_notLogged, Snackbar.LENGTH_LONG);
                mySnackbar.show();
            }
        } else if (id == R.id.Exit) {
            finish();
            System.exit(0);
        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    @Override
    public void onResume (){
        TextView tv1 = (TextView) findViewById(R.id.textView);
        LoginStatusSingleton status = LoginStatusSingleton.getInstance();
        if (status.getStatus()) {
            tv1.setText(status.getCredentials().user);
        }
        invalidateOptionsMenu();
        super.onResume();
        return ;
    }

    public void onKeywordsClicked(View v) {
        if (LoginStatusSingleton.getInstance().getStatus()) {
            Intent intent = new Intent(this, UpdateKeysActivity.class);
            this.startActivity(intent);
        } else {
            Snackbar mySnackbar = Snackbar.make(findViewById(R.id.content_main), R.string.error_notLogged, Snackbar.LENGTH_LONG);
            mySnackbar.show();
        }
    }

}
