package com.jjdcorp.juvenalduarte.investmentadvisor;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.annotation.TargetApi;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import com.jjdcorp.juvenalduarte.investmentadvisor.LoginActivity;

public class SubscribeActivity extends AppCompatActivity {

    // UI references.
    protected Button mSubmmitButton;
    private EditText mUserIDView;
    private EditText mPasswordView;
    private EditText mKeywordsView;
    private EditText mNKeywordsView;
    private View mProgressView;
    private View mRegisterFormView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_subscribe);

        // Retrieve already filled data from login form
        Intent intent = getIntent();
        String email = intent.getStringExtra("user");

        // Accessing edit text objects
        mUserIDView = (EditText) findViewById(R.id.editTextUserId);
        mUserIDView.setText((CharSequence) email);
        mUserIDView.invalidate();

        mPasswordView = (EditText) findViewById(R.id.editTextPassword);
        mPasswordView.requestFocus();

        mKeywordsView = (EditText) findViewById(R.id.editTextKeywords);
        mNKeywordsView = (EditText) findViewById(R.id.editTextNKeywords);

        // Defining a listener for the button
        mSubmmitButton = (Button) findViewById(R.id.credentialsSubmitButton);
        mSubmmitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                attemptRegisterNewUser();
            }
        });

        mRegisterFormView = findViewById(R.id.register_form);
        mProgressView = findViewById(R.id.register_progress);
    }

    /**
     * Shows the progress UI and hides the login form.
     */
    @TargetApi(Build.VERSION_CODES.HONEYCOMB_MR2)
    private void showProgress(final boolean show) {
        // On Honeycomb MR2 we have the ViewPropertyAnimator APIs, which allow
        // for very easy animations. If available, use these APIs to fade-in
        // the progress spinner.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.HONEYCOMB_MR2) {
            int shortAnimTime = getResources().getInteger(android.R.integer.config_shortAnimTime);

            mRegisterFormView.setVisibility(show ? View.GONE : View.VISIBLE);
            mRegisterFormView.animate().setDuration(shortAnimTime).alpha(
                    show ? 0 : 1).setListener(new AnimatorListenerAdapter() {
                @Override
                public void onAnimationEnd(Animator animation) {
                    mRegisterFormView.setVisibility(show ? View.GONE : View.VISIBLE);
                }
            });

            mProgressView.setVisibility(show ? View.VISIBLE : View.GONE);
            mProgressView.animate().setDuration(shortAnimTime).alpha(
                    show ? 1 : 0).setListener(new AnimatorListenerAdapter() {
                @Override
                public void onAnimationEnd(Animator animation) {
                    mProgressView.setVisibility(show ? View.VISIBLE : View.GONE);
                }
            });
        } else {
            // The ViewPropertyAnimator APIs are not available, so simply show
            // and hide the relevant UI components.
            mProgressView.setVisibility(show ? View.VISIBLE : View.GONE);
            mRegisterFormView.setVisibility(show ? View.GONE : View.VISIBLE);
        }
    }

    public class UserSubscribeTask extends AsyncTask<Void, Void, Integer> {
        private final String email;
        private final String password;
        private final String keywords;
        private final String nkeywords;

        public UserSubscribeTask(String email, String password, String keywords, String nkeywords) {
            this.email = email;
            this.password = password;
            this.keywords = keywords;
            this.nkeywords = nkeywords;
        }

        @Override
        protected Integer doInBackground(Void... params) {
            ServerSubscribe aServerSubs = new ServerSubscribe(this.email, this.password, this.keywords, this.nkeywords);
            int regStatus = aServerSubs.Register();
            return regStatus;
        }

        @Override
        protected void onPostExecute(final Integer success) {
            showProgress(false);

            if (success == 0) {
                LoginStatusSingleton logInStatus = LoginStatusSingleton.getInstance();
                logInStatus.logIn();
                logInStatus.setCredentials(new ServerLogIn(this.email, this.password));

                String keys = this.keywords + "|" + this.nkeywords;
                logInStatus.setKeywords(keys);
                finish();
                onBackPressed();

            } else if (success == 1){
                mUserIDView.setError(getString(R.string.error_register_exists));
                mUserIDView.requestFocus();
            } else {
                Snackbar mySnackbar = Snackbar.make(findViewById(R.id.register_form), R.string.error_unable2register, Snackbar.LENGTH_LONG);
                mySnackbar.show();
            }

        }

        @Override
        protected void onCancelled() {
            showProgress(false);
        }
    }

    private void attemptRegisterNewUser() {
        // Store values at the time of the login attempt.
        String sUserId = mUserIDView.getText().toString();
        String sPasswd = mPasswordView.getText().toString();
        String sKeyWrd = mKeywordsView.getText().toString();
        String sNKeyWrd = mNKeywordsView.getText().toString();

        boolean cancel = false;
        View focusView = null;

        // Check for a valid password, if the user entered one.
        if (!TextUtils.isEmpty(sPasswd) && !LoginActivity.isPasswordValid(sPasswd)) {
            mPasswordView.setError(getString(R.string.error_invalid_password));
            focusView = mPasswordView;
            cancel = true;
        }

        // Check for a valid email address.
        if (TextUtils.isEmpty(sUserId)) {
            mUserIDView.setError(getString(R.string.error_field_required));
            focusView = mUserIDView;
            cancel = true;
        } else if (!LoginActivity.isEmailValid(sUserId)) {
            mUserIDView.setError(getString(R.string.error_invalid_email));
            focusView = mUserIDView;
            cancel = true;
        }

        if (cancel) {
            // There was an error; don't attempt login and focus the first
            // form field with an error.
            focusView.requestFocus();
        } else {
            showProgress(true);
            UserSubscribeTask tskRegister = new UserSubscribeTask(sUserId, sPasswd, sKeyWrd, sNKeyWrd);
            tskRegister.execute();
        }
    }
}
