{-# LANGUAGE CPP #-}
{-# LANGUAGE NoRebindableSyntax #-}
{-# OPTIONS_GHC -fno-warn-missing-import-lists #-}
module Paths_caesoma (
    version,
    getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir,
    getDataFileName, getSysconfDir
  ) where

import qualified Control.Exception as Exception
import Data.Version (Version(..))
import System.Environment (getEnv)
import Prelude

#if defined(VERSION_base)

#if MIN_VERSION_base(4,0,0)
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#else
catchIO :: IO a -> (Exception.Exception -> IO a) -> IO a
#endif

#else
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#endif
catchIO = Exception.catch

version :: Version
version = Version [0,1,0,0] []
bindir, libdir, dynlibdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "/Users/soutomaiormenc2/git/hakyll/caesoma.github.io/src/.stack-work/install/x86_64-osx/lts-12.9/8.4.3/bin"
libdir     = "/Users/soutomaiormenc2/git/hakyll/caesoma.github.io/src/.stack-work/install/x86_64-osx/lts-12.9/8.4.3/lib/x86_64-osx-ghc-8.4.3/caesoma-0.1.0.0-1vZBpqg3KqQAOEzFlyvdPN-site"
dynlibdir  = "/Users/soutomaiormenc2/git/hakyll/caesoma.github.io/src/.stack-work/install/x86_64-osx/lts-12.9/8.4.3/lib/x86_64-osx-ghc-8.4.3"
datadir    = "/Users/soutomaiormenc2/git/hakyll/caesoma.github.io/src/.stack-work/install/x86_64-osx/lts-12.9/8.4.3/share/x86_64-osx-ghc-8.4.3/caesoma-0.1.0.0"
libexecdir = "/Users/soutomaiormenc2/git/hakyll/caesoma.github.io/src/.stack-work/install/x86_64-osx/lts-12.9/8.4.3/libexec/x86_64-osx-ghc-8.4.3/caesoma-0.1.0.0"
sysconfdir = "/Users/soutomaiormenc2/git/hakyll/caesoma.github.io/src/.stack-work/install/x86_64-osx/lts-12.9/8.4.3/etc"

getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "caesoma_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "caesoma_libdir") (\_ -> return libdir)
getDynLibDir = catchIO (getEnv "caesoma_dynlibdir") (\_ -> return dynlibdir)
getDataDir = catchIO (getEnv "caesoma_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "caesoma_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "caesoma_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "/" ++ name)
