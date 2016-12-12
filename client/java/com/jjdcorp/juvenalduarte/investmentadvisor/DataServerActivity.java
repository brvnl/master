package com.jjdcorp.juvenalduarte.investmentadvisor;

import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.Snackbar;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;

/**
 * Created by juvenalduarte on 20/11/16.
 */

public class DataServerActivity extends AppCompatActivity {
    private View mProgressViewNews;
    private View mNewsFormView;
    public ProgressDialog progressDialog;
    private boolean serverReady;
    private Object serverReadyLock = new Object();
    private boolean articleReady;
    private Object articleReadyLock = new Object();
    private ViewPager mViewPager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    public class DataServerFetchTask extends AsyncTask<Void, Void, Boolean> {
        private String email;
        private String password;

        public DataServerFetchTask(String email, String password) {
            this.email = email;
            this.password = password;
        }

        @Override
        protected Boolean doInBackground(Void... params) {
            ServerData userStore = ServerData.getInstance();
            userStore.fetchArticles(this.email, this.password);
            return true;
        }

        @Override
        protected void onPostExecute(final Boolean success) {
            setServerStatus();
            awakeServer();
            if (!success) {
                //Snackbar mySnackbar = Snackbar.make(findViewById(R.id.newsview1_form), R.string.error_server_failed, Snackbar.LENGTH_LONG);
                //mySnackbar.show();
            } else {
                mViewPager.invalidate();
                finish();
                startActivity(getIntent());
            }
        }

        @Override
        protected void onCancelled() {
            setServerStatus();
            awakeServer();
        }
    }

    public synchronized void setServerStatus() {
        synchronized (serverReadyLock) {
            serverReady = (ServerData.getInstance().countArticles() == -1) ? false : true;
        }
    }

    public synchronized boolean getServerStatus() {
        synchronized (serverReadyLock) {
            return serverReady;
        }
    }

    public synchronized void setArticleStatus(boolean status) {
        synchronized (articleReadyLock) {
            articleReady = status;
        }
    }

    public synchronized boolean getArticleStatus() {
        synchronized (articleReadyLock) {
            return articleReady;
        }
    }

    public synchronized void waitServer (String message) {
        if (progressDialog == null) {
            progressDialog = new ProgressDialog(this);
            progressDialog.setMessage(message);
            progressDialog.setIndeterminate(false);
            progressDialog.setCancelable(false);
            progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
            progressDialog.show();
        }
    }

    public synchronized void awakeServer () {
        if (progressDialog != null) {
            progressDialog.dismiss();
            progressDialog = null;
        }
    }
}
