package com.jjdcorp.juvenalduarte.investmentadvisor;

import android.app.ProgressDialog;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.preference.PreferenceManager;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;

import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;

import android.webkit.WebView;
import android.widget.TextView;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class NewsViewer1Activity extends AppCompatActivity {
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
        setContentView(R.layout.activity_news_viewer1);

        SharedPreferences preferences = PreferenceManager.getDefaultSharedPreferences(this);
        String allFeeders = "bloomberg.comOV=I=XseparatorX=I=VObr.advfn.comOV=I=XseparatorX=I=VOeconomist.comOV=I=XseparatorX=I=VOestadao.com.brOV=I=XseparatorX=I=VOforbes.comOV=I=XseparatorX=I=VOg1.globo.comOV=I=XseparatorX=I=VOinvestors.comOV=I=XseparatorX=I=VOnasdaq.comOV=I=XseparatorX=I=VOreuters.comOV=I=XseparatorX=I=VOtheguardian.comOV=I=XseparatorX=I=VOthestreet.comOV=I=XseparatorX=I=VOuol.com.br";
        String feeders_text = preferences.getString("mlist_feeders", allFeeders);
        int timewindow = Integer.parseInt(preferences.getString("edit_timewindow","7"));

        setServerStatus();
        if (!getServerStatus()){
            ServerLogIn servConn = LoginStatusSingleton.getInstance().getCredentials();
            DataServerFetchTask fetchTsk = new DataServerFetchTask(servConn.user,servConn.password, feeders_text, timewindow);
            fetchTsk.execute();
            waitServer("Fetching articles from server...");
        }

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
    }

    @Override
    protected void onResume() {
        super.onResume();
        // Create the adapter that will return a fragment for each of the three
        // primary sections of the activity.
        mSectionsPagerAdapter = new SectionsPagerAdapter(getSupportFragmentManager());

        // Set up the ViewPager with the sections adapter.
        mViewPager = (ViewPager) findViewById(R.id.container);
        mViewPager.setAdapter(mSectionsPagerAdapter);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_news_viewer1, menu);
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

    /**
     * A placeholder fragment containing a simple view.
     */
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
            View rootView = inflater.inflate(R.layout.fragment_news_viewer1, container, false);
            TextView textView = (TextView) rootView.findViewById(R.id.section_label);
            WebView fText = (WebView) rootView.findViewById(R.id.news_fulltext);
            TextView urlView = (TextView) rootView.findViewById(R.id.news_url);
            TextView timeView = (TextView) rootView.findViewById(R.id.news_timestamp);

            String fullTextHtml = txtToHtml(getArguments().getString("text"));

            textView.setText(getArguments().getString("title"));
            //fText.loadData(fullTextHtml, "text/html", null);
            fText.loadDataWithBaseURL(null, fullTextHtml, "text/html", "utf-8", null);
            urlView.setText(getArguments().getString("url"));
            timeView.setText(getArguments().getString("time"));
            //textView.setText(getString(R.string.section_format, getArguments().getInt(ARG_SECTION_NUMBER)));
            return rootView;
        }
    }

    /**
     * A {@link FragmentPagerAdapter} that returns a fragment corresponding to
     * one of the sections/tabs/pages.
     */
    public class SectionsPagerAdapter extends FragmentPagerAdapter {

        public SectionsPagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public Fragment getItem(int position) {
            // getItem is called to instantiate the fragment for the given page.
            // Return a PlaceholderFragment (defined as a static inner class below).
            PlaceholderFragment tabFrag = PlaceholderFragment.newInstance(position + 1);
            String title, text, url, time;
            // If article store is ready
            if (getServerStatus()) {
                Article current = getFullArticle(position);
                title = current.title;
                text = current.text;
                url = current.url;

                SimpleDateFormat input = new SimpleDateFormat("yyyyMMddhhmmss");
                SimpleDateFormat output = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");

                try {
                    time =  output.format(input.parse(current.timestamp));
                } catch (ParseException e) {
                    e.printStackTrace();
                    time = "9999-99-99 99:99:99";
                }
            } else {
                title = "";
                text = "";
                url = "";
                time = "";
            }

            Bundle bundle = new Bundle();
            bundle.putString("title", title);
            bundle.putString("text", text);
            bundle.putString("url", url);
            bundle.putString("time", time);
            tabFrag.setArguments(bundle);
            return tabFrag;
        }

        @Override
        public int getCount() {
            if (getServerStatus()) {
                return ServerData.getInstance().countArticles();
            } else {
                return 1;
            }
        }

        @Override
        public CharSequence getPageTitle(int position) {
            switch (position) {
                case 0:
                    return "SECTION 1";
                case 1:
                    return "SECTION 2";
                case 2:
                    return "SECTION 3";
            }
            return null;
        }
    }


    public Article getFullArticle(int index){
        // Retrieving article at the specific index...
        ServerData usrStore = ServerData.getInstance();
        return usrStore.getArticle(index);
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
                Snackbar mySnackbar = Snackbar.make(findViewById(R.id.newsview1_form), R.string.error_server_failed, Snackbar.LENGTH_LONG);
                mySnackbar.show();
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
            progressDialog = new ProgressDialog(NewsViewer1Activity.this);
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

    public static String txtToHtml(String s) {
        StringBuilder builder = new StringBuilder();
        boolean previousWasASpace = false;

        // Header
        builder.append("<html><body>");
        builder.append("<p align=\"justify\">");

        for (char c : s.toCharArray()) {
            if (c == ' ') {
                if (previousWasASpace) {
                    builder.append("&nbsp;");
                    previousWasASpace = false;
                    continue;
                }
                previousWasASpace = true;
            } else {
                previousWasASpace = false;
            }
            switch (c) {
                case '<':
                    builder.append("&lt;");
                    break;
                case '>':
                    builder.append("&gt;");
                    break;
                case '&':
                    builder.append("&amp;");
                    break;
                case '"':
                    builder.append("&quot;");
                    break;
                case '\n':
                    builder.append("<br>");
                    break;
                case '\t':
                    builder.append("&nbsp; &nbsp; &nbsp;");
                    break;
                default:
                    builder.append(c);

            }
        }

        // Footer
        builder.append("</p>");
        builder.append("</body></html>");

        String converted = builder.toString();
        String str = "(?i)\\b((?:https?://|www\\d{0,3}[.]|[a-z0-9.\\-]+[.][a-z]{2,4}/)(?:[^\\s()<>]+|\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\))+(?:\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\)|[^\\s`!()\\[\\]{};:\'\".,<>?«»“”‘’]))";
        Pattern patt = Pattern.compile(str);
        Matcher matcher = patt.matcher(converted);
        converted = matcher.replaceAll("<a href=\"$1\">$1</a>");

        // Highlight keywords
        String[] keys = LoginStatusSingleton.getInstance().keywords.split(", ");
        String regex = "("  + TextUtils.join("|", keys) + ")";
        Pattern pattrn = Pattern.compile(regex);
        Matcher matchr = pattrn.matcher(converted);
        converted = matchr.replaceAll("<mark>$1</mark>");

        return converted;
    }

}
