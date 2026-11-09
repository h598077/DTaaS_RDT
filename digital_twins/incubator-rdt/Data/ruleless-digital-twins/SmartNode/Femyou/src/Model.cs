using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.IO.Compression;
using System.Security.Cryptography;
using Femyou.Internal;
using static Femyou.IModel;

namespace Femyou
{
  public class Model
  {
    public static bool FreshFMUs =
      Environment.GetEnvironmentVariable("RDT_FEMYOU_FRESHFMUS") is not null;

    public static IModel Load(string fmuPath)
    {
      return Load(fmuPath, new Collection<UnsupportedFunctions>((UnsupportedFunctions[])Enum.GetValues(typeof(UnsupportedFunctions))));
    }
    public static IModel Load(string fmuPath, Collection<UnsupportedFunctions> unsupportedFunctions)
    {
      var TmpFolder = GetFreshTmpPath(fmuPath);
      ZipFile.ExtractToDirectory(fmuPath, TmpFolder, true);
      return new ModelImpl(TmpFolder, unsupportedFunctions);
    }

    public static IModel Load(Stream fmuStream, string fmuPath)
    {
      var TmpFolder = GetFreshTmpPath(fmuPath);
      ZipFile.ExtractToDirectory(fmuStream, TmpFolder, true);
      return new ModelImpl(TmpFolder, new Collection<UnsupportedFunctions>((UnsupportedFunctions[])Enum.GetValues(typeof(UnsupportedFunctions))));
    }

    private static string GetFreshTmpPath(string fmuPath)
    {
      string TmpFolder;
      /* Roll a fresh temporary folder everytime if you need to work around dynamic library issues.
      TODO: Since we don't have a proper destructor, it's up to the user to clean up the directory,
      so we keep on rolling fresh ones, which shouldn't really happen so often. */
      do
      {
        List<string> paths = [Path.GetTempPath(), nameof(Femyou), Path.GetFileName(fmuPath)];
        if (FreshFMUs)
        {
          paths.Insert(2, RandomNumberGenerator.GetString(
            choices: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            length: 5));
        }
        TmpFolder = Path.Combine(paths.ToArray());
      } while (FreshFMUs && Directory.Exists(TmpFolder));
      return TmpFolder;
    }
  }
}
