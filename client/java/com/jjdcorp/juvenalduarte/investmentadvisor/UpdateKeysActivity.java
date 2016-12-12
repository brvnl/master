package com.jjdcorp.juvenalduarte.investmentadvisor;

import android.app.ProgressDialog;
import android.graphics.Color;
import android.os.AsyncTask;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class UpdateKeysActivity extends AppCompatActivity {
    public ProgressDialog progressDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_update_keys);

        LoginStatusSingleton status = LoginStatusSingleton.getInstance();
        if (status.getStatus()) {
            String kwordsStr = status.getKeywords();
            kwordsStr = kwordsStr.replace(", ", ",");
            String[] keywords = kwordsStr.split("\\|", -1);

            TextView mNewPosKeys = (TextView) findViewById(R.id.editTextPosKeys);
            TextView mNewNegKeys = (TextView) findViewById(R.id.editTextNegKeys);
            mNewPosKeys.setText(keywords[0]);
            mNewNegKeys.setText(keywords[1]);
        }
    }

    public void onSubmmitClicked(View v) {
        TextView mNewPosKeys = (TextView) findViewById(R.id.editTextPosKeys);
        TextView mNewNegKeys = (TextView) findViewById(R.id.editTextNegKeys);

        String posKeys = mNewPosKeys.getText().toString();
        String negKeys = mNewNegKeys.getText().toString();

        ServerLogIn status = LoginStatusSingleton.getInstance().getCredentials();
        UpdateKeysTask updteTask = new UpdateKeysTask(status.user, status.password, posKeys, negKeys);
        waitServer("Updating keywords, waiting server response...");
        updteTask.execute();
    }

    public class UpdateKeysTask extends AsyncTask<Void, Void, Integer> {
        private final String email;
        private final String password;
        private final String keywords;
        private final String nkeywords;

        public UpdateKeysTask(String email, String password, String keywords, String nkeywords) {
            this.email = email;
            this.password = password;
            this.keywords = keywords;
            this.nkeywords = nkeywords;
        }

        @Override
        protected Integer doInBackground(Void... params) {
            ServerSubscribe aServerSubs = new ServerSubscribe(this.email, this.password, this.keywords, this.nkeywords);
            int regStatus = aServerSubs.Update();
            return regStatus;
        }

        @Override
        protected void onPostExecute(final Integer success) {
            awakeServer();

            if (success == 0) {
                LoginStatusSingleton logInStatus = LoginStatusSingleton.getInstance();

                String newKeywords = this.keywords.replace(",", ", ") + "|" + this.nkeywords.replace(",", ", ");
                logInStatus.setKeywords(newKeywords);
                ServerData.reset();
                finish();
                onBackPressed();

            } else {
                TextView mNewPosKeys = (TextView) findViewById(R.id.editTextPosKeys);
                mNewPosKeys.setError(getString(R.string.error_register_exists));
                mNewPosKeys.requestFocus();
            }

        }

        @Override
        protected void onCancelled() {
            awakeServer();
        }
    }

    public synchronized void waitServer (String message) {
        if (progressDialog == null) {
            progressDialog = new ProgressDialog(UpdateKeysActivity.this);
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
