import { useState } from "react";
import {
  useTable,
  tableFeatures,
  rowPaginationFeature,
  rowSortingFeature,
  columnFilteringFeature,
  type ColumnDef,
  type PaginationState,
  type SortingState,
} from "@tanstack/react-table";

// 使用する機能を登録
const features = tableFeatures({
  rowPaginationFeature,
  rowSortingFeature,
  columnFilteringFeature,
});

// データ型
export type ListedIssue = {
  code?: string;
  name?: string;
};

// カラム定義
const columns: ColumnDef<typeof features, ListedIssue>[] = [
  { accessorKey: "code", header: "銘柄コード" },
  { accessorKey: "name", header: "銘柄名" },
];

type Props = {
  items: ListedIssue[];
  total: number;
};

export function ListedIssueTable({ items, total }: Props) {
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 20,
  });
  console.log(items);
  const [sorting, setSorting] = useState<SortingState>([]);

  const table = useTable({
    features,
    data: items,
    columns,

    rowCount: total,

    manualPagination: true,
    manualSorting: true,
    manualFiltering: true,

    state: {
      pagination,
      sorting,
    },

    onPaginationChange: setPagination,
    onSortingChange: setSorting,
  });

  return (
    <>
      <table>
        <thead>
          {table.getHeaderGroups().map((group) => (
            <tr key={group.id}>
              {group.headers.map((header) => (
                <th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                >
                  <table.FlexRender header={header} />
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getAllCells().map((cell) => (
                <td key={cell.id}>
                  <table.FlexRender cell={cell} />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <button
        onClick={() => table.previousPage()}
        disabled={!table.getCanPreviousPage()}
      >
        前へ
      </button>

      <span>
        {pagination.pageIndex + 1} / {table.getPageCount()}
      </span>

      <button
        onClick={() => table.nextPage()}
        disabled={!table.getCanNextPage()}
      >
        次へ
      </button>
    </>
  );
}
