package com.jjdcorp.juvenalduarte.investmentadvisor;

/**
 * Created by juvenalduarte on 23/10/16.
 */

public class LoginStatusSingleton {
    private static LoginStatusSingleton instance = null;
    protected ServerLogIn credentials;
    protected boolean status;
    protected String keywords;

    protected LoginStatusSingleton() {
        status = false;
    }

    public static LoginStatusSingleton getInstance() {
        if(instance == null) {
            instance = new LoginStatusSingleton();
        }
        return instance;
    }

    public void logIn() {
        status = true;
        return;
    }

    public void logOut() {
        status = false;
        return;
    }

    public boolean getStatus() {
        return status;
    }

    public boolean setCredentials(ServerLogIn theCredentials) {
        if (theCredentials != null) {
            credentials = theCredentials;
            return true;
        } else {
            return false;
        }
    }

    public boolean setKeywords(String keys){
        if (keys.isEmpty()) {
            return false;
        } else {
            this.keywords = keys;
            return true;
        }
    }

    public String getKeywords() {
        return keywords;
    }

    public ServerLogIn getCredentials() {
        return credentials;
    }
}