package com.jjdcorp.juvenalduarte.investmentadvisor;

import android.app.ProgressDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.preference.PreferenceManager;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

public class SumaryViewActivity extends AppCompatActivity {
    private View mProgressViewNews;
    private View mNewsFormView;
    public ProgressDialog progressDialog;
    private boolean serverReady;
    private Object serverReadyLock = new Object();
    private boolean articleReady;
    private Object articleReadyLock = new Object();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sumary_view);

        SharedPreferences preferences = PreferenceManager.getDefaultSharedPreferences(this);
        String allFeeders = "bloomberg.comOV=I=XseparatorX=I=VObr.advfn.comOV=I=XseparatorX=I=VOeconomist.comOV=I=XseparatorX=I=VOestadao.com.brOV=I=XseparatorX=I=VOforbes.comOV=I=XseparatorX=I=VOg1.globo.comOV=I=XseparatorX=I=VOinvestors.comOV=I=XseparatorX=I=VOnasdaq.comOV=I=XseparatorX=I=VOreuters.comOV=I=XseparatorX=I=VOtheguardian.comOV=I=XseparatorX=I=VOthestreet.comOV=I=XseparatorX=I=VOuol.com.br";
        String feeders_text = preferences.getString("mlist_feeders", allFeeders);
        int timewindow = Integer.parseInt(preferences.getString("edit_timewindow","7"));

        ArrayList<HashMap<String,String>> list = new ArrayList<HashMap<String,String>>();
        String[] values = {"waiting server..."};

        setServerStatus();
        if (!getServerStatus()){
            ServerLogIn servConn = LoginStatusSingleton.getInstance().getCredentials();
            DataServerFetchTask fetchTsk = new DataServerFetchTask(servConn.user,servConn.password, feeders_text, timewindow);
            waitServer("Fetching articles from server...");
            fetchTsk.execute();

        } else {
            ServerData dataprovider = ServerData.getInstance();
            values = new String[dataprovider.countArticles()];
            Iterator<Article> it = dataprovider.articles.iterator();
            int index = 0;
            String time;
            while (it.hasNext()) {
                HashMap<String,String> temp = new HashMap<String,String>();

                Article current = it.next();

                SimpleDateFormat input = new SimpleDateFormat("yyyyMMddhhmmss");
                SimpleDateFormat output = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");

                try {
                    time =  output.format(input.parse(current.timestamp));
                } catch (ParseException e) {
                    e.printStackTrace();
                    time = "9999-99-99 99:99:99";
                }

                //values[index++] = "(" + time + ") " + current.title;
                String[] sourcepath = current.id.split("\\/");
                String source = sourcepath[sourcepath.length - 2];

                temp.put("timestamp",time);
                temp.put("source", source);
                temp.put("title", current.title);
                list.add(temp);
            }
        }

        // Get ListView object from xml
        ListView listView = (ListView) findViewById(R.id.newslist);

        SimpleAdapter adapter = new SimpleAdapter(
                this,
                list,
                R.layout.activity_sumary_row_view,
                new String[] {"timestamp","source","title"},
                new int[] {R.id.ltime,R.id.lsource, R.id.ltitle}
        );

        /*ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_list_item_1, android.R.id.text1, values);*/
        listView.setAdapter(adapter);

        // ListView Item Click Listener
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> parent, View view,
                                    int position, long id) {

                Intent intent = new Intent(SumaryViewActivity.this, ArticleViewerActivity.class);
                intent.putExtra("article_index", position);
                startActivity(intent);
            }
        });
    }

    public class DataServerFetchTask extends AsyncTask<Void, Void, Boolean> {
        private String email;
        private String password;
        private String feeders;
        private int timewindow;

        public DataServerFetchTask(String email, String password, String feeders, int tw) {
            this.email = email;
            this.password = password;
            this.feeders = feeders;
            this.timewindow = tw;
        }

        @Override
        protected Boolean doInBackground(Void... params) {
            ServerData userStore = ServerData.getInstance();
            userStore.fetchArticles(this.email, this.password, this.feeders, this.timewindow);
            return true;
        }

        @Override
        protected void onPostExecute(final Boolean success) {
            setServerStatus();
            awakeServer();
            if (!success) {
                Snackbar mySnackbar = Snackbar.make(findViewById(R.id.activity_sumary_view), R.string.error_server_failed, Snackbar.LENGTH_LONG);
                mySnackbar.show();
            } else {
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
            progressDialog = new ProgressDialog(SumaryViewActivity.this);
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
