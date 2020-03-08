module Semantic.CLI.Spec (testTree) where

import           Analysis.File
import           Control.Carrier.Parse.Simple
import           Control.Carrier.Reader
import           Data.ByteString.Builder
import           Data.Language
import           Semantic.Api hiding (Blob, BlobPair, File)
import           Semantic.Task
import           Serializing.Format
import           System.IO.Unsafe
import           System.Path ((</>))
import qualified System.Path as Path
import qualified System.Path.Directory as Path

import SpecHelpers
import Test.Tasty
import Test.Tasty.Golden

testTree :: TestTree
testTree = testGroup "Semantic.CLI"
  [ testGroup "parseDiffBuilder" $ fmap testForDiffFixture diffFixtures
  , testGroup "parseTermBuilder" $ fmap testForParseFixture parseFixtures
  ]

-- We provide this function to the golden tests so as to have better
-- output when diffing JSON outputs. If you're investigating these
-- tests and find this output hard to read, install the `jd` CLI tool
-- (https://github.com/josephburnett/jd), which will print a detailed
-- summary of the differences between these JSON files.
renderDiff :: String -> String -> [String]
renderDiff ref new = unsafePerformIO $ do
  useJD <- (Path.hasExtension ".json" (Path.relPath ref) &&) <$> fmap isJust (Path.findExecutable "jd")
  pure $ if useJD
    then ["jd", "-set", ref, new]
    else ["git", "diff", ref, new]
{-# NOINLINE renderDiff #-}

testForDiffFixture :: (String, [BlobPair] -> ParseC TaskC Builder, [(File Language, File Language)], Path.RelFile) -> TestTree
testForDiffFixture (diffRenderer, runDiff, files, expected) =
  goldenVsStringDiff
    ("diff fixture renders to " <> diffRenderer <> " " <> show files)
    renderDiff
    (Path.toString expected)
    (fmap toLazyByteString . runTaskOrDie $ readBlobPairs (Right files) >>= runDiff)

testForParseFixture :: (String, [Blob] -> ParseC TaskC Builder, [File Language], Path.RelFile) -> TestTree
testForParseFixture (format, runParse, files, expected) =
  goldenVsStringDiff
    ("diff fixture renders to " <> format)
    renderDiff
    (Path.toString expected)
    (fmap toLazyByteString . runTaskOrDie $ readBlobs (FilesFromPaths files) >>= runParse)

parseFixtures :: [(String, [Blob] -> ParseC TaskC Builder, [File Language], Path.RelFile)]
parseFixtures =
  [ ("s-expression", run . parseTermBuilder TermSExpression, path, Path.relFile "test/fixtures/ruby/corpus/and-or.parseA.txt")
  , ("json", run . parseTermBuilder TermJSONTree, path, prefix </> Path.file "parse-tree.json")
  , ("json", run . parseTermBuilder TermJSONTree, path', prefix </> Path.file "parse-trees.json")
  , ("json", run . parseTermBuilder TermJSONTree, [], prefix </> Path.file "parse-tree-empty.json")
  , ("symbols", run . parseSymbolsBuilder Serializing.Format.JSON, path'', prefix </> Path.file "parse-tree.symbols.json")
  , ("protobuf symbols", run . parseSymbolsBuilder Serializing.Format.Proto, path'', prefix </> Path.file "parse-tree.symbols.protobuf.bin")
  ]
  where path = [File (Path.absRel "test/fixtures/ruby/corpus/and-or.A.rb") lowerBound Ruby]
        path' = [File (Path.absRel "test/fixtures/ruby/corpus/and-or.A.rb") lowerBound Ruby, File (Path.absRel"test/fixtures/ruby/corpus/and-or.B.rb") lowerBound Ruby]
        path'' = [File (Path.absRel "test/fixtures/ruby/corpus/method-declaration.A.rb") lowerBound Ruby]
        prefix = Path.relDir "test/fixtures/cli"
        run = runReader defaultLanguageModes

diffFixtures :: [(String, [BlobPair] -> ParseC TaskC Builder, [(File Language, File Language)], Path.RelFile)]
diffFixtures =
  [ ("json diff", parseDiffBuilder DiffJSONTree, pathMode, prefix </> Path.file "diff-tree.json")
  , ("s-expression diff", parseDiffBuilder DiffSExpression, pathMode, Path.relFile "test/fixtures/ruby/corpus/method-declaration.diffA-B.txt")
  , ("toc summaries diff", runReader aLaCarteLanguageModes . diffSummaryBuilder Serializing.Format.JSON, pathMode, prefix </> Path.file "diff-tree.toc.json")
  , ("protobuf diff", runReader aLaCarteLanguageModes . diffSummaryBuilder Serializing.Format.Proto, pathMode, prefix </> Path.file "diff-tree.toc.protobuf.bin")
  ]
  where pathMode = [(File (Path.absRel "test/fixtures/ruby/corpus/method-declaration.A.rb") lowerBound Ruby, File (Path.absRel "test/fixtures/ruby/corpus/method-declaration.B.rb") lowerBound Ruby)]
        prefix = Path.relDir "test/fixtures/cli"
