package com.jjdcorp.juvenalduarte.investmentadvisor;

import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Looper;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.app.FragmentStatePagerAdapter;
import android.support.v4.view.ViewPager;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.ProgressBar;
import android.widget.TextView;


public class NewsActivity extends AppCompatActivity {
    private View mProgressViewNews;
    private View mNewsFormView;
    private static final int SERVER_TIMEOUT = 120000;
    public ProgressDialog progressDialog;
    private boolean serverReady;
    private Object serverReadyLock = new Object();
    private boolean articleReady;
    private Object articleReadyLock = new Object();

    /**
     * The {@link android.support.v4.view.PagerAdapter} that will provide
     * fragments for each of the sections. We use a
     * {@link FragmentPagerAdapter} derivative, which will keep every
     * loaded fragment in memory. If this becomes too memory intensive, it
     * may be best to switch to a
     * {@link android.support.v4.app.FragmentStatePagerAdapter}.
     */
    private SectionsPagerAdapter mSectionsPagerAdapter;

    /**
     * The {@link ViewPager} that will host the section contents.
     */
    private ViewPager mViewPager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_news);

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        // Create the adapter that will return a fragment for each of the three
        // primary sections of the activity.
        mSectionsPagerAdapter = new SectionsPagerAdapter(getSupportFragmentManager());

        // Set up the ViewPager with the sections adapter.
        mViewPager = (ViewPager) findViewById(R.id.container);
        mViewPager.setAdapter(mSectionsPagerAdapter);

        mNewsFormView = findViewById(R.id.news_form);
        mProgressViewNews = findViewById(R.id.news_progress);
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
            progressDialog = new ProgressDialog(NewsActivity.this);
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

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_news, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
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
            if (success) {
                //finish();

            } else {
                Snackbar mySnackbar = Snackbar.make(findViewById(R.id.news_form), R.string.error_server_failed, Snackbar.LENGTH_LONG);
                mySnackbar.show();
            }
        }

        @Override
        protected void onCancelled() {
            setServerStatus();
            awakeServer();
        }
    }


    public class DataServerDownloadTask extends AsyncTask<Void, Void, Boolean> {
        Article article2download;

        public DataServerDownloadTask(Article anArticle){
            this.article2download = anArticle;
        }

        @Override
        protected Boolean doInBackground(Void... params) {
            return ServerData.getInstance().downloadArticle(this.article2download);
        }

        @Override
        protected void onPostExecute(final Boolean success) {
            awakeServer();
            if (success) {
                //finish();

            } else {
                Snackbar mySnackbar = Snackbar.make(findViewById(R.id.news_form), R.string.error_server_failed, Snackbar.LENGTH_LONG);
                mySnackbar.show();
            }
        }

        @Override
        protected void onCancelled() {
            awakeServer();
        }
    }

    public Article getFullArticle(int index){
        // Retrieving article at the specific index...
        ServerData usrStore = ServerData.getInstance();
        Article currentArticle = usrStore.getArticle(index);

        if (!currentArticle.isDownloaded()) {
            // Downloading full text
            DataServerDownloadTask downloadTask = new DataServerDownloadTask(currentArticle);

            // Forces main thread to wait until data is fetch from server
            setArticleStatus(false);
            downloadTask.execute();
        } else {
            setArticleStatus(true);
        }

        return currentArticle;
    }

    /**
     * A placeholder fragment containing a simple view.
     */
    //public class PlaceholderFragment extends Fragment {
    public static class PlaceholderFragment extends Fragment {
        /**
         * The fragment argument representing the section number for this
         * fragment.
         */
        private static final String ARG_SECTION_NUMBER = "section_number";

        public PlaceholderFragment() {
        }

        /**
         * Returns a new instance of this fragment for the given section
         * number.
         */
        public static PlaceholderFragment newInstance(int sectionNumber) {
            PlaceholderFragment fragment = new PlaceholderFragment();
            Bundle args = new Bundle();
            args.putInt(ARG_SECTION_NUMBER, sectionNumber);
            fragment.setArguments(args);
            return fragment;
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                                 Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_news, container, false);
            TextView textView = (TextView) rootView.findViewById(R.id.section_label);
            textView.setText(getString(R.string.section_format, getArguments().getInt(ARG_SECTION_NUMBER)));
            return rootView;
        }
    }

    /**
     * A {@link FragmentPagerAdapter} that returns a fragment corresponding to
     * one of the sections/tabs/pages.
     */
    public class SectionsPagerAdapter extends FragmentStatePagerAdapter {
    //public class SectionsPagerAdapter extends FragmentPagerAdapter {

        public SectionsPagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public Fragment getItem(int position) {
            // getItem is called to instantiate the fragment for the given page.
            // Return a PlaceholderFragment (defined as a static inner class below).
            PlaceholderFragment newFragment = PlaceholderFragment.newInstance(position + 1);
            //notifyDataSetChanged();
            return newFragment;
        }

        @Override
        public int getCount() {
            // Show 3 total pages.
            return 3;
        }

        @Override
        public CharSequence getPageTitle(int position) {
            switch (position) {
                case 0:
                    return "Noticia 1";
                case 1:
                    return "Noticia 2";
                case 2:
                    return "Noticia 3";
            }
            return null;
        }
    }
}
