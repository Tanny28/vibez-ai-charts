import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';

export const Profile: React.FC = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleLogout = async () => {
    setLoading(true);
    await signOut();
    navigate('/login');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 relative overflow-hidden">
      {/* Animated background orbs */}
      <motion.div
        className="absolute w-96 h-96 bg-indigo-500/30 rounded-full blur-3xl"
        animate={{
          x: [0, 50, 0],
          y: [0, -80, 0],
          scale: [1, 1.15, 1],
        }}
        transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
        style={{ top: '10%', left: '20%' }}
      />
      <motion.div
        className="absolute w-96 h-96 bg-pink-500/30 rounded-full blur-3xl"
        animate={{
          x: [0, -50, 0],
          y: [0, 80, 0],
          scale: [1, 1.25, 1],
        }}
        transition={{ duration: 23, repeat: Infinity, ease: 'linear' }}
        style={{ bottom: '10%', right: '20%' }}
      />

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <button
            onClick={() => navigate('/')}
            className="text-white/70 hover:text-white flex items-center gap-2 mb-4 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Dashboard
          </button>
          <h1 className="text-4xl font-bold text-white">Profile Settings</h1>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-6 max-w-4xl">
          {/* Account Information Card */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl shadow-2xl shadow-black/30 p-6"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-pink-500 rounded-full flex items-center justify-center text-white text-xl font-bold">
                {user?.email?.charAt(0).toUpperCase()}
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Account Info</h2>
                <p className="text-sm text-white/60">Your profile details</p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-white/60 mb-1">Full Name</label>
                <div className="px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white">
                  {user?.user_metadata?.full_name || 'Not set'}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-white/60 mb-1">Email Address</label>
                <div className="px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white">
                  {user?.email}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-white/60 mb-1">User ID</label>
                <div className="px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white text-sm font-mono truncate">
                  {user?.id}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-white/60 mb-1">Member Since</label>
                <div className="px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white">
                  {user?.created_at ? formatDate(user.created_at) : 'Unknown'}
                </div>
              </div>
            </div>
          </motion.div>

          {/* Actions Card */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl shadow-2xl shadow-black/30 p-6"
          >
            <h2 className="text-xl font-bold text-white mb-6">Quick Actions</h2>

            <div className="space-y-4">
              {/* Email Verified Status */}
              <div className="p-4 bg-white/5 border border-white/20 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-white font-medium">Email Verification</p>
                    <p className="text-sm text-white/60">
                      {user?.email_confirmed_at ? 'Verified' : 'Not verified'}
                    </p>
                  </div>
                  {user?.email_confirmed_at ? (
                    <div className="w-8 h-8 bg-green-500/20 rounded-full flex items-center justify-center">
                      <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  ) : (
                    <div className="w-8 h-8 bg-yellow-500/20 rounded-full flex items-center justify-center">
                      <svg className="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                    </div>
                  )}
                </div>
              </div>

              {/* Sign in method */}
              <div className="p-4 bg-white/5 border border-white/20 rounded-lg">
                <p className="text-white font-medium mb-1">Sign-in Method</p>
                <div className="flex items-center gap-2">
                  {user?.app_metadata?.provider === 'google' ? (
                    <>
                      <svg className="w-5 h-5" viewBox="0 0 24 24">
                        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                      </svg>
                      <span className="text-white/80">Google</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                      <span className="text-white/80">Email/Password</span>
                    </>
                  )}
                </div>
              </div>

              {/* Logout Button */}
              <motion.button
                onClick={handleLogout}
                disabled={loading}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full py-3 bg-gradient-to-r from-red-600 to-pink-600 text-white font-semibold rounded-lg shadow-lg shadow-red-500/30 hover:shadow-red-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                {loading ? 'Signing out...' : 'Sign Out'}
              </motion.button>
            </div>
          </motion.div>
        </div>

        {/* Usage Stats Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl shadow-2xl shadow-black/30 p-6 mt-6 max-w-4xl"
        >
          <h2 className="text-xl font-bold text-white mb-4">✨ Your Vibez AI Journey</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-lg border border-white/10">
              <p className="text-white/60 text-sm mb-1">Account Type</p>
              <p className="text-2xl font-bold text-white">Free Tier</p>
            </div>
            <div className="p-4 bg-gradient-to-br from-green-500/20 to-blue-500/20 rounded-lg border border-white/10">
              <p className="text-white/60 text-sm mb-1">Status</p>
              <p className="text-2xl font-bold text-green-400">Active</p>
            </div>
            <div className="p-4 bg-gradient-to-br from-pink-500/20 to-orange-500/20 rounded-lg border border-white/10">
              <p className="text-white/60 text-sm mb-1">AI Provider</p>
              <p className="text-2xl font-bold text-white">Gemini 2.5</p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};
