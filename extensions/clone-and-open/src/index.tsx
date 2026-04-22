import {
  ActionPanel,
  Action,
  Form,
  getPreferenceValues,
  popToRoot,
  showToast,
  Toast,
} from "@raycast/api";
import { execFile } from "child_process";
import { homedir } from "os";
import { join } from "path";
import { existsSync } from "fs";
import { promisify } from "util";
import { useState } from "react";

const execFileAsync = promisify(execFile);

// Prepend common install locations so CLI tools are found regardless of how Raycast launches
const PATH_ENV = `/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:${process.env.PATH ?? ""}`;

interface Preferences {
  devFolder: string;
  editor: string;
}

function expandHome(p: string): string {
  return p.startsWith("~") ? homedir() + p.slice(1) : p;
}

function repoNameFromUrl(url: string): string {
  return (
    url
      .trim()
      .replace(/\/$/, "")
      .replace(/\.git$/, "")
      .split("/")
      .pop() ?? "repo"
  );
}

export default function CloneRepository() {
  const { devFolder, editor } = getPreferenceValues<Preferences>();
  const [urlError, setUrlError] = useState<string | undefined>();

  async function handleSubmit(values: { url: string }) {
    const url = values.url.trim();

    if (!url) {
      setUrlError("Required");
      return;
    }

    const repoName = repoNameFromUrl(url);
    const targetPath = join(expandHome(devFolder), repoName);

    if (existsSync(targetPath)) {
      setUrlError(`Directory already exists: ${targetPath}`);
      return;
    }

    const toast = await showToast({
      style: Toast.Style.Animated,
      title: "Cloning…",
      message: repoName,
    });

    try {
      await execFileAsync("git", ["clone", url, targetPath], {
        env: { ...process.env, PATH: PATH_ENV },
      });

      toast.title = "Opening in editor…";
      await execFileAsync(editor, [targetPath], {
        env: { ...process.env, PATH: PATH_ENV },
      });

      toast.style = Toast.Style.Success;
      toast.title = "Done";
      toast.message = `Opened ${repoName}`;

      await popToRoot();
    } catch (err) {
      toast.style = Toast.Style.Failure;
      toast.title = "Failed";
      toast.message = err instanceof Error ? err.message : String(err);
    }
  }

  return (
    <Form
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Clone & Open" onSubmit={handleSubmit} />
        </ActionPanel>
      }
    >
      <Form.TextField
        id="url"
        title="Repository URL"
        placeholder="https://github.com/owner/repo"
        autoFocus
        error={urlError}
        onChange={() => setUrlError(undefined)}
      />
    </Form>
  );
}
